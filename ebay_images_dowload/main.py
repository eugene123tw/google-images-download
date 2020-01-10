import os
import datetime
import requests

from ebaysdk.finding import Connection as finding
from ebaysdk.shopping import Connection as shopping

class EbayDownload:
    yaml = './ebay.yaml'
    finding_api = finding()
    shopping_api =shopping()
    def __init__(self, num_items=100):
        """
        Args:
            keywords (list):
            num_items (int):
        """
        pass

    def search_keyword(self, keywords, pageNumber=1, categoryId=-1):
        response = self.finding_api.execute('findItemsAdvanced', {
                                                'keywords': keywords,
                                                'categoryId': categoryId,
                                                'paginationInput': {
                                                    'pageNumber': pageNumber
                                                }
                                            })
        assert (response.reply.ack == 'Success')
        assert (type(response.reply.timestamp) == datetime.datetime)
        assert (type(response.reply.searchResult.item) == list)
        return response

    def search_category(self, categoryId, pageNumber):
        response = self.finding_api.execute('findItemsByCategory', {
            'categoryId': categoryId,
            'paginationInput': {
                'pageNumber': pageNumber
            }
        })
        return response.reply.searchResult

    def get_categories(self):
        response = self.shopping_api.execute('GetCategoryInfo',
                                             {'CategoryID': -1, 'IncludeSelector': 'ChildCategories'})
        for category in response.reply.CategoryArray.Category:
            if category.get('CategoryIDPath'):
                print("Category: {} ({})".format(category.CategoryName, category.CategoryID))

    def get_category(self, category_id):
        """

        Args:
            category_id (int):
        Returns:
        """
        self._recur_category(category_id, '')


    def _recur_category(self, category_id, tabs):
        response = self.shopping_api.execute('GetCategoryInfo', {'CategoryID': category_id, 'IncludeSelector': 'ChildCategories'})
        if int(response.reply.CategoryCount) > 1:
            tabs += '\t'
            for category in response.reply.CategoryArray.Category:
                if int(category.CategoryID) != int(category_id) :
                    print("{}{} ({})".format(tabs, category.CategoryName, category.CategoryID))
                    self._recur_category(category.CategoryID, tabs)

    def download_product_image(self, searchResult):
        chunks = lambda lst: [(yield lst[i:i + 20]) for i in range(0, len(lst), 20)]

        def _download_image(ebay_product, path='.'):
            item_id = ebay_product.ItemID
            image_urls = ebay_product.PictureURL
            save_dir = os.path.join(os.path.expanduser(path), 'download_image')
            os.makedirs(save_dir, exist_ok=True)
            for i, image_url in enumerate(image_urls):
                img_data = requests.get(image_url).content
                basename = str(item_id) + '_' + str(i+1) + '.jpg'
                save_path = os.path.join(save_dir, basename)
                with open(save_path, 'wb') as handler:
                    handler.write(img_data)

        items = searchResult.item
        for item_list in chunks(items):
            itemIds = [item.itemId for item in item_list]
            response = self.shopping_api.execute('GetMultipleItems', {'ItemID': itemIds })

            for ebay_product in response.reply.Item:
                _download_image(ebay_product)

        print('finished')


if __name__ == '__main__':
    ebay = EbayDownload()

    searchResult = ebay.search_category(categoryId=246, pageNumber=3)
    ebay.download_product_image(searchResult)

