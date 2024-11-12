import os

from django.conf import settings
from django.core.files.storage import DefaultStorage
from filebrowser.sites import FileBrowserSite as OriginalFileBrowserSite


class FileBrowserSite(OriginalFileBrowserSite):
    def browse(self, request):
        # get directory path from settings to avoid recursion
        self.directory = settings.FILEBROWSER_DIRECTORY + str(request.user.pk) + "/"
        # create a directory for a user if it does not already exist
        full_path = self.storage.location + "/" + self.directory
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        return super().browse(request)


storage = DefaultStorage()
site = FileBrowserSite(name="file", storage=storage)
