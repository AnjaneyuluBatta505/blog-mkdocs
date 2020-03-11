from mkdocs.utils import meta
from mkdocs.plugins import BasePlugin


class Blog(BasePlugin):

    def change_dest_path_for_blog(self, file_obj):
        abs_dest_path = file_obj.abs_dest_path
        abs_dest_path = re.sub(r'\d{4}-\d{2}-\d{2}\_', '', abs_dest_path)
        file_obj.abs_dest_path = abs_dest_path
        dest_path = re.sub(r'\d{4}-\d{2}-\d{2}\_', '', dest_path)
        file_obj.dest_path = dest_path
        print("*" * 10, file_obj.abs_dest_path, file_obj.dest_path)

    def get_meta_data(self, path):
        with open(path, 'r') as f:
            _, mdata = meta.get_data(f.read())
            if mdata.get('date_published', None) is None:
                raise Exception(
                    'File {} is missing field `date_published`'.format(path))
            return mdata
        return {}

    def get_latest_blog_artices(self, blog_data):
        sort_key = 'date_published'
        blog_articles = sorted(blog_data, key=lambda obj: obj[sort_key], reverse=True)
        return blog_articles[:10]

    def on_page_context(self, context, **kwargs):
        blog_data = []
        pages = context['pages']
        for file_obj in pages:
            if file_obj.src_path.startswith('blog/'):
                self.change_dest_path_for_blog(file_obj)
                meta_data = self.get_meta_data(file_obj.abs_src_path)
                blog_data.append(meta_data)
        context['latest_blog_artices'] = self.get_latest_blog_artices(
            blog_data)
        print("#" * 100)
        print(context['latest_blog_artices'])
        return context
