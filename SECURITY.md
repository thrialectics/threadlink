# 🛡️ Security Policy

## 🚨 Reporting Security Vulnerabilities

If you discover a security vulnerability in Threadlink, please report it responsibly:

1. **DO NOT** open a public issue for security vulnerabilities
2. Email security concerns to: [your-security-email@example.com]
3. Include detailed steps to reproduce the issue
4. Allow reasonable time for a fix before public disclosure

## 🔒 Security Considerations

### Data Privacy

Threadlink is designed to be **local-first** and **privacy-respecting**:

- ✅ All data stored locally in `~/.threadlink/`
- ✅ No data transmitted to external services
- ✅ Chat URLs are stored as provided (not accessed automatically)
- ⚠️ **Your thread index contains sensitive file paths and URLs**

### File System Security

**Important:** Threadlink accesses your local file system:

- Files are accessed with your user permissions
- No automatic file content reading or modification
- Be cautious when linking sensitive files
- Consider using relative paths when possible

### Chat URL Security

**Warning:** Chat URLs may contain sensitive information:

- Some chat platforms include conversation content in share URLs
- Shared URLs might be accessible to others
- Consider using private/limited-access sharing options

## 🛡️ Security Best Practices

### For Users

1. **Secure your thread index**:
   ```bash
   chmod 600 ~/.threadlink/thread_index.json
   ```

2. **Use relative paths when possible**:
   ```bash
   # Better
   threadlink attach project_x ./notes.md
   
   # Avoid if possible
   threadlink attach project_x /Users/yourname/sensitive/file.txt
   ```

3. **Review chat URLs before adding**:
   - Ensure URLs don't expose sensitive content
   - Use private sharing options when available
   - Consider removing or anonymizing old URLs

4. **Regular cleanup**:
   ```bash
   # Review your stored data periodically
   cat ~/.threadlink/thread_index.json
   ```

### For Developers

1. **Input validation**:
   - Validate file paths and URLs
   - Sanitize user input before JSON storage
   - Implement path traversal protection

2. **File access controls**:
   - Restrict file operations to expected directories
   - Validate file extensions and types
   - Implement proper error handling

3. **Data storage**:
   - Use secure file permissions
   - Consider encryption for sensitive data
   - Implement backup and recovery procedures

## 🔍 Known Security Limitations

1. **No encryption**: Thread data is stored in plain JSON
2. **No access controls**: Any process with user permissions can read thread data
3. **URL validation**: Limited validation of chat URLs
4. **Path traversal**: Basic protection against directory traversal

## 🚀 Future Security Enhancements

- [ ] Optional encryption for thread index
- [ ] Enhanced URL validation and sanitization
- [ ] Configurable file access restrictions
- [ ] Audit logging for sensitive operations
- [ ] Integration with system keychain for sensitive URLs

## 🏗️ Secure Development Guidelines

### Dependencies
- Regularly audit dependencies: `pip audit`
- Pin dependency versions in production
- Review dependency licenses and security records

### Code Review
- All security-related changes require review
- Test security features with edge cases
- Validate input handling and error cases

### Testing
- Include security test cases
- Test with malformed input
- Verify file permission handling

## 📋 Security Checklist for Contributors

Before submitting security-related changes:

- [ ] Input validation implemented
- [ ] Error handling covers edge cases
- [ ] No sensitive data in test files
- [ ] File permissions properly set
- [ ] Documentation updated for security implications

## 🆔 Security Contact

For security-related questions or concerns:
- **Email**: [your-security-email@example.com]
- **PGP Key**: [Optional PGP key ID]
- **Response time**: We aim to respond within 48 hours

---

**Remember**: Threadlink handles your personal conversation history and file paths. Always review what data you're storing and sharing. 