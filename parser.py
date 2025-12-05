def file2dict(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as file:
            doc_id = -1
            content_lines = []
            timeout = False
            for line in file:
                if line.startswith('<doc'):
                    id_start = line.find('"')
                    id_end = line.find('"', id_start+1)
                    doc_id = int(line[id_start+1:id_end])
                elif line.startswith('<timeout>'):
                    timeout_start = line.find('>')
                    timeout = False if line[timeout_start+1] == '0' else True
                elif line.startswith('<model'):
                    # parse model name
                    pass
                elif line.startswith('<duration'):
                    dur_start = line.find('"')
                    dur_end = line.find('"', dur_start+1)
                    duration = (line[dur_start+1:dur_end])
                elif line.startswith('</doc'):
                    doc_dict = {
                        'id': doc_id,
                        'content': content_lines,
                        'timeout': timeout,
                    }
                    yield doc_dict
                    # reset variables
                    doc_id = -1
                    content_lines = []
                    timeout = False
                elif line.startswith('<'):
                    # skip lines with tag
                    continue
                else:
                    line = line.removesuffix('\n')
                    if line:
                        content_lines.append(line)
            if doc_id != -1:
                doc_dict = {
                    'id': doc_id,
                    'content': content_lines,
                    'duration': duration,
                    'timeout': timeout,
                }
                yield doc_dict
    except FileNotFoundError:
        print(f'File {file_path} does not exists.')
        return
