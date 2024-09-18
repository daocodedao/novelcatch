


from douban import Douban


doub=Douban()
# 根据图书名搜索图书，选第一个结果
# doub.search(query="文学之冬", locale="cn")
# 直接输入图书ID，图书详情页URL里的 https://book.douban.com/subject/36486737/  36486737
doub._parse_single_book(id="36486737")
print("success")




