"""
Implementation of `FileRepositoryAdapter`, adapter that is used to handle file system directories.
"""

import glob
import os
from pathlib import Path


from .git_adapter import RepositoryAdapter

def remove_prefix(text, prefix):
    """
    Utility method to remove the prefix
    """
    if not isinstance(text, str):
        text=str(text)
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever


class FileRepositoryAdapter(RepositoryAdapter):    #pylint: disable=abstract-method
    """
    Implements all methods for file based repository. Using 'rsync' for this purpose.
    """

    @classmethod
    def fetch_command(cls):
        """
        Initial fetch of the repository.
        Return cmdline that has to be executed to fetch the repository.
        Skipping if `self._repository_url` is not specified
        """

        if not cls._repository_url:
            return None

        if not os.path.isdir(cls._repository_url):
            raise RuntimeError(
                "The repository '%s' has to be a valid directory location" % cls._repository_url)
        repository_url = cls._repository_url

        local_repository_dir = cls.local_repository_location()
        if not local_repository_dir:
            return None

        if not repository_url.endswith('/'):
            repository_url+='/'
        if local_repository_dir.endswith('/'):
            local_repository_dir=local_repository_dir[:-1]

        return ['rsync', '-rvtW', '--delete', '--modify-window=1', repository_url, local_repository_dir]

    @classmethod
    def update_command(cls):
        """
        Update of the repository.
        """

        return cls.fetch_command

    @classmethod
    def current_state_command(cls):
        """
        Current state is the latest modified time of a file.
        """

        if not cls._repository_url:
            return None

        local_repository_dir = cls.local_repository_location()
        if not local_repository_dir:
            return None

        paths = sorted(Path(local_repository_dir).iterdir(), key=os.path.getmtime, reverse=True)

        # returning the latest modification date
        return os.path.getmtime(paths[0]) if paths else None

    @classmethod
    def get_updates_list(cls, updated_files_list):
        """
        Return the list of the files changed since the last update
        """
        local_repository_dir = cls.local_repository_location()
        if not local_repository_dir:
            return None

        current_state = cls.get_state()
        paths = sorted(Path(local_repository_dir).iterdir(), key=os.path.getmtime, reverse=True)

        answer = []
        if not current_state:
            answer = [item.resolve() for item in paths]
        else:
            # all files with modified date bigger than the saved state
            answer = [item for item in paths if current_state < os.path.getmtime(item)]


        if not local_repository_dir.endswith('/'):
            local_repository_dir+='/'
        return [remove_prefix(item, local_repository_dir) for item in answer]
