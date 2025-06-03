import argparse
import json
import uuid
import datetime
import re 
from pathlib import Path

def get_thread_index():
    """Load or create the thread index"""
    base_dir = Path.home() / ".threadlink"
    index_file = base_dir / "thread_index.json"
    base_dir.mkdir(parents=True, exist_ok=True)
    
    if index_file.exists():
        with open(index_file, "r") as f:
            return json.load(f), index_file
    else:
        return {}, index_file

def save_index(thread_index, index_file):
    """Save the thread index"""
    with open(index_file, "w") as f:
        json.dump(thread_index, f, indent=2)

def slugify(text, max_words=3, max_chars=25):
    """Create a clean slug from text"""
    words = re.findall(r'\w+', text.lower())
    slug = "_".join(words[:max_words])
    return slug[:max_chars]

def new_thread(args):
    """Create a new thread entry"""
    thread_index, index_file = get_thread_index()
    
    thread_id = args.tag or str(uuid.uuid4())
    entry = {
        "summary": args.summary or "",
        "linked_files": [],
        "chat_url": args.chat_url or "",
        "date_created": datetime.datetime.now().isoformat(),
        "auto_generated": not args.tag
    }
    thread_index[thread_id] = entry
    save_index(thread_index, index_file)
    print(f"New thread created: {thread_id}")

def attach_file(args):
    """Attach a file to a thread"""
    thread_index, index_file = get_thread_index()
    
    thread_id = args.tag
    if thread_id not in thread_index:
        print(f"Thread ID '{thread_id}' not found.")
        return

    resolved_path = str(Path(args.file).expanduser().resolve())
    if not Path(resolved_path).exists():
        print(f"⚠️  Warning: File '{resolved_path}' does not exist.")
        return

    files = thread_index[thread_id].get("linked_files", [])
    if resolved_path not in files:
        files.append(resolved_path)
        thread_index[thread_id]["linked_files"] = files
        save_index(thread_index, index_file)
        print(f"✅ File '{resolved_path}' attached to thread '{thread_id}'.")
    else:
        print(f"ℹ️  File '{resolved_path}' is already linked to thread '{thread_id}'.")

def show_thread(args):
    """Show thread details"""
    thread_index, index_file = get_thread_index()
    
    thread_id = args.tag
    if thread_id in thread_index:
        print(json.dumps(thread_index[thread_id], indent=2))
    else:
        print(f"Thread ID '{thread_id}' not found.")

def search_threads(args):
    """Search threads by keyword"""
    thread_index, index_file = get_thread_index()
    
    query = args.query.lower()
    results = {
        k: v for k, v in thread_index.items()
        if query in k.lower() or query in v.get("summary", "").lower()
    }
    if results:
        print(json.dumps(results, indent=2))
    else:
        print("No matching threads found.")

def reverse_lookup(args):
    """Find thread linked to a file"""
    thread_index, index_file = get_thread_index()
    
    file_path = args.file
    for thread_id, thread_data in thread_index.items():
        if isinstance(thread_data, dict) and "linked_files" in thread_data:
            if file_path in thread_data["linked_files"]:
                print(json.dumps({
                    "thread_id": thread_id,
                    "summary": thread_data.get("summary", ""),
                    "chat_url": thread_data.get("chat_url", ""),
                    "file_path": file_path
                }, indent=2))
                return
    print(json.dumps({"error": "No thread found for this file."}, indent=2))

def quick_thread(args):
    """Quickly create a new thread entry with auto-generated tag"""
    thread_index, index_file = get_thread_index()
    
    base_slug = slugify(args.summary)
    today = datetime.date.today().isoformat()
    thread_id = f"{base_slug}_{today}"
    
    # Handle duplicates
    i = 1
    original_id = thread_id
    while thread_id in thread_index:
        i += 1
        thread_id = f"{original_id}_{i}"

    entry = {
        "summary": args.summary,
        "linked_files": [],
        "chat_url": args.chat_url or "",
        "date_created": datetime.datetime.now().isoformat(),
        "auto_generated": True
    }
    thread_index[thread_id] = entry
    save_index(thread_index, index_file)
    print(f"Thread created: {thread_id}")
    print(f"Summary: {args.summary}")
    print(f"Chat URL: {args.chat_url}")

def detach_file(args):
    """Remove a file from a thread"""
    thread_index, index_file = get_thread_index()
    
    thread_id = args.tag
    if thread_id not in thread_index:
        print(f"Thread ID '{thread_id}' not found.")
        return

    files = thread_index[thread_id].get("linked_files", [])
    if args.file in files:
        files.remove(args.file)
        thread_index[thread_id]["linked_files"] = files
        save_index(thread_index, index_file)
        print(f"File '{args.file}' detached from thread '{thread_id}'.")
    else:
        print(f"File '{args.file}' is not linked to thread '{thread_id}'.")

def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description="Threadlink CLI Tool")
    subparsers = parser.add_subparsers()

    # New thread command
    parser_new = subparsers.add_parser("new", help="Create a new thread entry")
    parser_new.add_argument("--tag", help="Custom thread tag (optional)")
    parser_new.add_argument("--summary", help="Short summary of the thread")
    parser_new.add_argument("--chat_url", help="Link to the chat")
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
    parser_search.add_argument("query", help="Keyword to search")
    parser_search.set_defaults(func=search_threads)

    # Reverse lookup command
    parser_reverse = subparsers.add_parser("reverse", help="Find thread linked to a file")
    parser_reverse.add_argument("file", help="Path to the file to look up")
    parser_reverse.set_defaults(func=reverse_lookup)

    # Quick thread command
    parser_quick = subparsers.add_parser("quick", help="Quickly create a new thread entry with auto-generated tag")
    parser_quick.add_argument("summary", help="Summary of the thread")
    parser_quick.add_argument("chat_url", help="Chat URL")
    parser_quick.set_defaults(func=quick_thread)

    # Parse and execute
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()