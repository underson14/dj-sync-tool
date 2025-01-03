from xml.dom import minidom
from xml.dom.minidom import Element

from app.models.PlaylistModel import PlaylistModel
from app.models.rekordbox.Track import Track
from app.readers.BaseReader import BaseReader


class TrackReader(BaseReader):
    def __init__(self, path):
        super().__init__(path)
        self.__playlist: PlaylistModel | None = None

    def read(self):
        files = []
        collection = minidom.parse(self._path).getElementsByTagName('COLLECTION')[0]
        for node in collection.childNodes:
            if not isinstance(node, Element) or node.nodeName != 'TRACK' or not self.__allowed_track(node):
                continue

            music_file = Track(node).decode()
            if not music_file.is_file():
                self._logger().warning(f'File {music_file.filename()} does not exists at path {music_file.location}')
                continue

            files.append(music_file)

        self._logger().info(f'Found {len(files)} tracks!')
        self._logger().info(f'--------------------------')

        return files

    def __allowed_track(self, node: Element):
        return self.__playlist.has_track(int(node.attributes['TrackID'].value))

    def set_playlist(self, playlist: PlaylistModel):
        self._logger().info(f'Using playlist: {playlist.name}')
        self.__playlist = playlist
