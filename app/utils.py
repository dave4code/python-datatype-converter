def get_file_extension(filename):
    """
    Extract file extension from filename
    
    Args:
        filename: Name of the file
        
    Returns:
        str: File extension without the dot
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''
