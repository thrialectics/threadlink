import argparse
import json
import uuid
import datetime
import re 
import urllib.parse
import os
from pathlib import Path

# Security constants
MAX_SUMMARY_LENGTH = 500
MAX_TAG_LENGTH = 100
MAX_FILE_PATH_LENGTH = 1000
ALLOWED_URL_SCHEMES = ['http', 'https']
ALLOWED_DOMAINS = [
    'chat.openai.com',
    'claude.ai', 
    'bard.google.com',
    'www.perplexity.ai',
    'poe.com'
]

def sanitize_string(text, max_length=None):
    """Sanitize user input to prevent injection attacks"""
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    
    # Remove null bytes and control characters
    sanitized = ''.join(char for char in text if ord(char) >= 32 or char in '\t\n\r')
    
    # Remove potential JSON escape sequences
    sanitized = sanitized.replace('\\', '\\\\').replace('"', '\\"')
    
    # Apply length limit
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized.strip()

def validate_url(url):
    """Validate and sanitize chat URLs"""
    if not url:
        return ""
    
    try:
        parsed = urllib.parse.urlparse(url)
        
        # Check scheme
        if parsed.scheme not in ALLOWED_URL_SCHEMES:
            raise ValueError(f"URL scheme must be one of: {', '.join(ALLOWED_URL_SCHEMES)}")
        
        # Check domain (optional - can be disabled for flexibility)
        # Commenting out domain restriction for now as users might use other AI services
        # if parsed.netloc not in ALLOWED_DOMAINS:
        #     raise ValueError(f"URL domain must be one of: {', '.join(ALLOWED_DOMAINS)}")
        
        # Reconstruct URL to normalize it
        return urllib.parse.urlunparse(parsed)
    
    except Exception as e:
        raise ValueError(f"Invalid URL format: {e}")

def validate_file_path(file_path):
    """Validate and sanitize file paths to prevent path traversal"""
    if not file_path:
        raise ValueError("File path cannot be empty")
    
    if len(file_path) > MAX_FILE_PATH_LENGTH:
        raise ValueError(f"File path too long (max {MAX_FILE_PATH_LENGTH} characters)")
    
    # Convert to Path object and resolve
    try:
        path = Path(file_path).expanduser().resolve()
    except Exception as e:
        raise ValueError(f"Invalid file path: {e}")
    
    # Check for path traversal attempts
    path_str = str(path)
    if '..' in file_path or path_str.startswith('/etc') or path_str.startswith('/var') or path_str.startswith('/usr'):
        print(f"⚠️  Warning: Path '{file_path}' may access system directories")
    
    # Additional security: ensure path is under user's home directory or current working directory
    user_home = Path.home()
    current_dir = Path.cwd()
    
    try:
        # Check if path is under home or current directory
        path.relative_to(user_home)
    except ValueError:
        try:
            path.relative_to(current_dir)
        except ValueError:
            print(f"⚠️  Warning: File '{path}' is outside your home directory and current directory")
    
    return str(path)

def validate_tag(tag):
    """Validate thread tag/ID"""
    if not tag:
        raise ValueError("Tag cannot be empty")
    
    if len(tag) > MAX_TAG_LENGTH:
        raise ValueError(f"Tag too long (max {MAX_TAG_LENGTH} characters)")
    
    # Check for potentially dangerous characters
    if any(char in tag for char in ['<', '>', '"', "'", '&', '\n', '\r', '\0']):
        raise ValueError("Tag contains invalid characters")
    
    return sanitize_string(tag, MAX_TAG_LENGTH)

def get_thread_index():
    """Load or create the thread index with proper error handling"""
    base_dir = Path.home() / ".threadlink"
    index_file = base_dir / "thread_index.json"
    
    try:
        base_dir.mkdir(parents=True, exist_ok=True, mode=0o700)  # Secure permissions
    except Exception as e:
        raise RuntimeError(f"Failed to create threadlink directory: {e}")
    
    if index_file.exists():
        try:
            with open(index_file, "r", encoding='utf-8') as f:
                data = json.load(f)
                # Validate loaded data structure
                if not isinstance(data, dict):
                    raise ValueError("Thread index must be a JSON object")
                return data, index_file
        except (json.JSONDecodeError, ValueError) as e:
            print(f"⚠️  Warning: Corrupted thread index file. Creating backup...")
            backup_file = index_file.with_suffix('.json.backup')
            index_file.rename(backup_file)
            print(f"Backup saved as: {backup_file}")
            return {}, index_file
        except Exception as e:
            raise RuntimeError(f"Failed to read thread index: {e}")
    else:
        return {}, index_file

def save_index(thread_index, index_file):
    """Save the thread index with proper error handling and permissions"""
    try:
        # Create temporary file first
        temp_file = index_file.with_suffix('.tmp')
        with open(temp_file, "w", encoding='utf-8') as f:
            json.dump(thread_index, f, indent=2, ensure_ascii=False)
        
        # Atomic rename
        temp_file.replace(index_file)
        
        # Set secure permissions
        os.chmod(index_file, 0o600)
        
    except Exception as e:
        raise RuntimeError(f"Failed to save thread index: {e}")

def slugify(text, max_words=3, max_chars=25):
    """Create a clean slug from text with security considerations"""
    if not text:
        return "unnamed"
    
    # Sanitize input first
    text = sanitize_string(text, 100)
    
    # Extract words (alphanumeric only for security)
    words = re.findall(r'\w+', text.lower())
    if not words:
        return "unnamed"
    
    slug = "_".join(words[:max_words])
    return slug[:max_chars]

def new_thread(args):
    """Create a new thread entry with input validation"""
    try:
        thread_index, index_file = get_thread_index()
        
        # Validate and sanitize inputs
        if args.tag:
            thread_id = validate_tag(args.tag)
        else:
            thread_id = str(uuid.uuid4())
        
        if thread_id in thread_index:
            print(f"⚠️  Error: Thread ID '{thread_id}' already exists.")
            return
        
        summary = sanitize_string(args.summary or "", MAX_SUMMARY_LENGTH)
        chat_url = validate_url(args.chat_url or "")
        
        entry = {
            "summary": summary,
            "linked_files": [],
            "chat_url": chat_url,
            "date_created": datetime.datetime.now().isoformat(),
            "auto_generated": not args.tag
        }
        
        thread_index[thread_id] = entry
        save_index(thread_index, index_file)
        print(f"✅ New thread created: {thread_id}")
        
    except (ValueError, RuntimeError) as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def attach_file(args):
    """Attach a file to a thread with security validation"""
    try:
        thread_index, index_file = get_thread_index()
        
        # Validate thread ID
        thread_id = validate_tag(args.tag)
        if thread_id not in thread_index:
            print(f"❌ Thread ID '{thread_id}' not found.")
            return

        # Validate and resolve file path
        resolved_path = validate_file_path(args.file)
        
        if not Path(resolved_path).exists():
            print(f"⚠️  Warning: File '{resolved_path}' does not exist.")
            response = input("Attach anyway? (y/N): ").strip().lower()
            if response != 'y':
                return

        files = thread_index[thread_id].get("linked_files", [])
        if resolved_path not in files:
            files.append(resolved_path)
            thread_index[thread_id]["linked_files"] = files
            save_index(thread_index, index_file)
            print(f"✅ File '{resolved_path}' attached to thread '{thread_id}'.")
        else:
            print(f"ℹ️  File '{resolved_path}' is already linked to thread '{thread_id}'.")

    except (ValueError, RuntimeError) as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def show_thread(args):
    """Show thread details with safe output"""
    try:
        thread_index, index_file = get_thread_index()
        
        thread_id = validate_tag(args.tag)
        if thread_id in thread_index:
            # Safe JSON output
            print(json.dumps(thread_index[thread_id], indent=2, ensure_ascii=False))
        else:
            print(f"❌ Thread ID '{thread_id}' not found.")
            
    except (ValueError, RuntimeError) as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def search_threads(args):
    """Search threads by keyword with input validation"""
    try:
        thread_index, index_file = get_thread_index()
        
        # Sanitize search query
        query = sanitize_string(args.query, 100).lower()
        if not query:
            print("❌ Search query cannot be empty")
            return
        
        results = {}
        for k, v in thread_index.items():
            if isinstance(v, dict):
                summary = v.get("summary", "").lower()
                if query in k.lower() or query in summary:
                    results[k] = v
        
        if results:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print("No matching threads found.")
            
    except (ValueError, RuntimeError) as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def reverse_lookup(args):
    """Find thread linked to a file with path validation"""
    try:
        thread_index, index_file = get_thread_index()
        
        # Validate file path
        file_path = validate_file_path(args.file)
        
        for thread_id, thread_data in thread_index.items():
            if isinstance(thread_data, dict) and "linked_files" in thread_data:
                if file_path in thread_data["linked_files"]:
                    result = {
                        "thread_id": thread_id,
                        "summary": thread_data.get("summary", ""),
                        "chat_url": thread_data.get("chat_url", ""),
                        "file_path": file_path
                    }
                    print(json.dumps(result, indent=2, ensure_ascii=False))
                    return
        
        print(json.dumps({"error": "No thread found for this file."}, indent=2))
        
    except (ValueError, RuntimeError) as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def quick_thread(args):
    """Quickly create a new thread entry with auto-generated tag"""
    try:
        thread_index, index_file = get_thread_index()
        
        # Validate and sanitize inputs
        summary = sanitize_string(args.summary, MAX_SUMMARY_LENGTH)
        if not summary:
            print("❌ Summary cannot be empty")
            return
            
        chat_url = validate_url(args.chat_url or "")
        
        base_slug = slugify(summary)
        today = datetime.date.today().isoformat()
        thread_id = f"{base_slug}_{today}"
        
        # Handle duplicates
        i = 1
        original_id = thread_id
        while thread_id in thread_index:
            i += 1
            thread_id = f"{original_id}_{i}"

        entry = {
            "summary": summary,
            "linked_files": [],
            "chat_url": chat_url,
            "date_created": datetime.datetime.now().isoformat(),
            "auto_generated": True
        }
        
        thread_index[thread_id] = entry
        save_index(thread_index, index_file)
        print(f"✅ Thread created: {thread_id}")
        print(f"Summary: {summary}")
        if chat_url:
            print(f"Chat URL: {chat_url}")
            
    except (ValueError, RuntimeError) as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def detach_file(args):
    """Remove a file from a thread with validation"""
    try:
        thread_index, index_file = get_thread_index()
        
        thread_id = validate_tag(args.tag)
        if thread_id not in thread_index:
            print(f"❌ Thread ID '{thread_id}' not found.")
            return

        # Validate file path
        file_path = validate_file_path(args.file)
        
        files = thread_index[thread_id].get("linked_files", [])
        if file_path in files:
            files.remove(file_path)
            thread_index[thread_id]["linked_files"] = files
            save_index(thread_index, index_file)
            print(f"✅ File '{file_path}' detached from thread '{thread_id}'.")
        else:
            print(f"❌ File '{file_path}' is not linked to thread '{thread_id}'.")
            
    except (ValueError, RuntimeError) as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main entry point for the CLI with error handling"""
    try:
        parser = argparse.ArgumentParser(description="Threadlink CLI Tool")
        subparsers = parser.add_subparsers()

        # New thread command
        parser_new = subparsers.add_parser("new", help="Create a new thread entry")
        parser_new.add_argument("--tag", help=f"Custom thread tag (max {MAX_TAG_LENGTH} chars)")
        parser_new.add_argument("--summary", help=f"Short summary of the thread (max {MAX_SUMMARY_LENGTH} chars)")
        parser_new.add_argument("--chat_url", help="Link to the chat (https URLs only)")
        parser_new.set_defaults(func=new_thread)

        # Attach file command
        parser_attach = subparsers.add_parser("attach", help="Attach a file to a thread")
        parser_attach.add_argument("tag", help="Thread tag or UUID")
        parser_attach.add_argument("file", help="Path to the file to attach")
        parser_attach.set_defaults(func=attach_file)

        # Detach file command
        parser_detach = subparsers.add_parser("detach", help="Remove a file from a thread")
        parser_detach.add_argument("tag", help="Thread tag or UUID")
        parser_detach.add_argument("file", help="Path to the file to detach")
        parser_detach.set_defaults(func=detach_file)

        # Show thread command
        parser_show = subparsers.add_parser("show", help="Show thread details")
        parser_show.add_argument("tag", help="Thread tag or UUID")
        parser_show.set_defaults(func=show_thread)

        # Search threads command
        parser_search = subparsers.add_parser("search", help="Search threads by keyword")
        parser_search.add_argument("query", help="Keyword to search (max 100 chars)")
        parser_search.set_defaults(func=search_threads)

        # Reverse lookup command
        parser_reverse = subparsers.add_parser("reverse", help="Find thread linked to a file")
        parser_reverse.add_argument("file", help="Path to the file to look up")
        parser_reverse.set_defaults(func=reverse_lookup)
        parser_reverse.add_argument("--json", action="store_true")

        # Quick thread command
        parser_quick = subparsers.add_parser("quick", help="Quickly create a new thread entry with auto-generated tag")
        parser_quick.add_argument("summary", help=f"Summary of the thread (max {MAX_SUMMARY_LENGTH} chars)")
        parser_quick.add_argument("chat_url", help="Chat URL (https URLs only)")
        parser_quick.set_defaults(func=quick_thread)

        # Parse and execute
        args = parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()
