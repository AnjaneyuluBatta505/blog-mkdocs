import re
from mkdocs.utils import meta
from mkdocs.plugins import BasePlugin


_date_format = r'\d{4}-\d{2}-\d{2}\_'


class Blog(BasePlugin):

    def __init__(self):
        self.blog_data = []
        self.latest_articles = []
        self.tags = {}

    def get_blog_data(self, files):
        blog_data = []
        for file_obj in files:
            if file_obj.src_path.startswith('blog/'):
                meta_data = self.get_meta_data(file_obj.abs_src_path)
                blog_data.append(meta_data)
        return blog_data

    def get_latest_articles(self, blog_data):
        sort_key = 'date_published'
        blog_articles = sorted(
            blog_data, key=lambda obj: obj[sort_key], reverse=True)
        return blog_articles[:10]

    def get_related_articles(self, page, blog_data):
        rel_articles = page.meta.get('related_articles', [])
        return tuple(filter(lambda x: x.get('title') in rel_articles, blog_data))

    def get_tags(self, blog_data):
        blog_tags = {}
        for mdata in blog_data:
            tags = mdata.get('tags', [])
            for tag in tags:
                tdata = blog_tags.get(tag) or []
                tdata.append(mdata)
                blog_tags[tag] = tdata
        return blog_tags

    def on_files(self, files, config):
        for file_obj in files:
            abs_dest_path = file_obj.abs_dest_path
            abs_dest_path = re.sub(_date_format, '', abs_dest_path)
            file_obj.abs_dest_path = abs_dest_path
            dest_path = file_obj.dest_path
            dest_path = re.sub(_date_format, '', dest_path)
            file_obj.dest_path = dest_path

            # blog meta data
            if file_obj.src_path.startswith('blog/'):
                meta_data = self.get_meta_data(file_obj.abs_src_path)
                meta_data['url'] = meta_data['path']
                self.blog_data.append(meta_data)
        self.latest_articles = self.get_latest_articles(self.blog_data)
        self.tags = self.get_tags(self.blog_data)

    def get_meta_data(self, path):
        with open(path, 'r') as f:
            _, mdata = meta.get_data(f.read())
            if mdata.get('date_published', None) is None:
                raise Exception(
                    'File {} is missing field `date_published`'.format(path))
            return mdata
        return {}

    def on_pre_page(self, page, config, files):
        if page.url.startswith('blog/'):
            url = re.sub(_date_format, '', page.url)
            page.file.url = url

    def on_page_context(self, context, page, config, nav, **kwargs):
        context['latest_articles'] = self.latest_articles
        related_articles = self.get_related_articles(page, self.blog_data)
        context['related_articles'] = related_articles
        context['blog_tags'] = self.tags
        return context
