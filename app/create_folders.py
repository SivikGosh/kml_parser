from souping_file import soup

async def create_placemark_folder(soup):
    w = get_line_width(soup, style)

    if 'line' in style:
        file_name = f'{legend[style]}_width_{w}'
    else:
        file_name = legend[style]
    
    if not os.path.isdir(file_name):
        os.mkdir(file_name)
    os.chdir(file_name)