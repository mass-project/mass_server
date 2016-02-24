import magic
import re
import os
from io import BufferedReader
from werkzeug.datastructures import FileStorage


class FileFunctions:
    @staticmethod
    def get_magic_string_from_file(file):
        if isinstance(file, BufferedReader):
            magic_string = magic.from_buffer(file.read()).decode('utf-8')
            file.seek(0)
            return magic_string
        else:
            raise TypeError('Unsupported file type: {}'.format(type(file)))

    @staticmethod
    def get_mime_type_from_file(file):
        if isinstance(file, BufferedReader):
            mime_string = magic.from_buffer(file.read(), mime=True).decode('utf-8')
            file.seek(0)
            return mime_string
        else:
            raise TypeError('Unsupported file type: {}'.format(type(file)))

    @staticmethod
    def get_file_extension(file_name):
        extension_regex = re.compile(r"\.([^.]+)$")
        match = re.search(extension_regex, file_name)

        # no match e.g. no "." in the file_path
        if match is None:
            return ""

        extension = match.group(1)
        return extension.lower()

    @staticmethod
    def get_file_size(file):
        if isinstance(file, BufferedReader):
            return os.path.getsize(file.name)
        else:
            raise TypeError('Unsupported file type: {}'.format(type(file)))

    @staticmethod
    def get_extra_tags_from_magic_string(magic_string):
        extra_tags = list()

        if re.search(r"PDF document", magic_string):
            extra_tags.append('filetype:pdf')

        if re.search(r"PE32 executable", magic_string):
            extra_tags.append('filetype:pe-32')
            extra_tags.append('filetype:windows-binary')

        if re.search(r"PE32\+ executable", magic_string):
            extra_tags.append('filetype:pe-64')
            extra_tags.append('filetype:windows-binary')

        if re.search(r"Microsoft Word", magic_string) or \
           re.search(r"Microsoft Excel", magic_string) or \
           re.search(r"Composite Document File", magic_string):
            extra_tags.append('filetype:ms-office')

        if re.search(r"capture file", magic_string):
            extra_tags.append('filetype:pcap')

        if re.search(r"HTML document", magic_string):
            extra_tags.append('filetype:html')

        if re.search(r"Java Jar file", magic_string) or \
            re.search(r"Java archive data", magic_string):
            extra_tags.append('filetype:java-jar')

        if re.search(r"Windows Registry", magic_string):
            extra_tags.append('filetype:windows-registry')

        if re.search(r"Zip archive", magic_string):
            extra_tags.append('filetype:archive')

        if re.search(r"Macromedia Flash data", magic_string):
            extra_tags.append('filetype:flash')

        return extra_tags

    @staticmethod
    def assemble_tag_list(magic_string, mime_type, file_extension):
        tags = list()
        if file_extension != '':
            tags.append('extension:' + file_extension)
        if mime_type != '':
            tags.append('mime:' + mime_type)
        extra_tags = FileFunctions.get_extra_tags_from_magic_string(magic_string)
        tags.extend(extra_tags)
        return tags

    @staticmethod
    def get_file_type(file):
        magic_string = FileFunctions.get_magic_string_from_file(file)
        tags = FileFunctions.get_extra_tags_from_magic_string(magic_string)
        if 'filetype:windows-binary' in tags:
            return 'windows-binary'
        else:
            return 'normal-file'

    @staticmethod
    def get_file_name(file):
        if isinstance(file, BufferedReader):
            return os.path.basename(file.name)
        else:
            raise TypeError('Unsupported file type: {}'.format(type(file)))

    # @staticmethod
    # def get_download_response_for_mongoengine_file_object(file):
    #     content = file.read()
    #     content_type = file.content_type
    #     response = HttpResponse(content, content_type=content_type)
    #     response['Content-Disposition'] = 'attachment; filename="{}"'.format(file.filename)
    #     return response
