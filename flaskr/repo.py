import os
import re
import itertools


class ImgRepo:
    _category_cache: dict

    def __init__(self):
        self._category_cache = self._create_category_mapping()

    def categories(self):
        return list(self._category_cache.keys())

    def files_in_category(self, category: str):
        return self._category_cache[category]

    @staticmethod
    def _create_category_mapping(rel_to_static_path: str = f"images"):
        curr_dirname = os.path.dirname(__file__)
        path = os.path.relpath(curr_dirname + os.path.sep + "static" + os.path.sep + rel_to_static_path)

        rec_search = os.walk(path)

        # creating paths relative to static-root
        files = [map(lambda fp: rel_to_static_path + os.path.sep + fp, files) for path, folders, files in rec_search]

        files = itertools.chain.from_iterable(files)

        mapped = map(ImgRepo._map_filename, files)

        grouped = {t[0]: list(map(lambda x: x['filename'], t[1])) for t in
                   itertools.groupby(mapped, key=lambda x: x['category'])}

        return grouped

    @staticmethod
    def _clean_category_name(category_name: str):
        return category_name.replace('_', ' ').title()

    @staticmethod
    def _map_filename(fname: str):
        pat = r"(?P<category>\w+)_(?P<num>\d+)\.jpg"
        splitted = fname.split(os.path.sep)
        filename = splitted[-1]
        m = re.match(pat, filename, re.RegexFlag.I)
        return {'category': ImgRepo._clean_category_name(m.group('category')), 'filename': fname.replace(os.path.sep, '/')}


if __name__ == "__main__":
    repo = ImgRepo()
    c = repo.categories()
    pass
