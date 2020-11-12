"""
Adapter for https://github.com/cheat/cheat

Cheatsheets are located in `cheat/cheatsheets/`
Each cheat sheet is a separate file without extension
"""

# pylint: disable=relative-import,abstract-method

from .file_adapter import FileRepositoryAdapter

class MyTest(FileRepositoryAdapter):
    """
    File at file  system
    """

    _adapter_name = "mytest"
    _output_format = "code"
    _cache_needed = True
    _repository_url = "/home/ochaloup/Dropbox/Knowledgebase/poznamky/knowledgebase-notes"
    _local_repository_location="knowledgebase-notes"
    _cheatsheet_files_prefix = ""
    _cheatsheet_files_extension = ".adoc"
