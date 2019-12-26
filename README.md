# -python-QQ音乐歌词爬虫-
一个课堂作业：动态爬取QQ音乐中“新裤子乐队”的歌词内容，切词后做成词云，以挖掘其歌词的关键内容。

“新裤子乐队”是我特别喜欢的中国摇滚乐队，我想试着分析他们的歌词内容。本来我想用requests+bs的方式提取静态内容，但发现QQ音乐官方网站中，歌词并不完全显示在页面中。这种动态显示的歌词显然不适合用bs来提取，只能用动态爬取的方式，于是确定了基本思路：在开发者工具中找到各歌曲歌词文件的url，再从中提取、清洗内容。

在某首歌的页面上，通过开发者工具我找到了对应的歌词文件。但点击其Request url 却无法进到真正的页面中，而是返回{"retcode":-1310,"code":-1310,"subcode":-1310}这一组信息。可见QQ音乐对歌词做了一些反爬处理，但经验告诉我，这些Request url一定有规律。

于是我看了几首歌的Request url和对应的字段参数，发现这个url只有一个“musicid”参数在变化，所以只要能拿到musicid就可以。同时，在网上查找相关经验贴时，有博主提醒QQ音乐在Request headers中会设置防盗链，即设置referer字段。

果不其然，referer的值中有一个变化的字段。其实referer指的是歌曲歌词页面的url，那这个变化的字段一定是上级页面（即歌手页页面）中给出的，几次比较分析发现，这个字段其实就是mid参数的值。所以，只要找到每首歌对应的mid、musicid两个参数的值，就可以获取到每首歌的歌词内容。那这些值在哪找呢？肯定是歌手页，所以我把歌手页所有的文件都看了下，发现了https://u.y.qq.com/cgi-bin/musicu.fcg?-=getSingerSong69405645034824&g_tk=480556310&loginUin=574294857&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22singerSongList%22%3A%7B%22method%22%3A%22GetSingerSongList%22%2C%22param%22%3A%7B%22order%22%3A1%2C%22singerMid%22%3A%22000keDtj2Um0rT%22%2C%22begin%22%3A0%2C%22num%22%3A10%7D%2C%22module%22%3A%22musichall.song_list_server%22%7D%7D 这个文件，里面放置了我们需要的所有信息。

这下就万事俱备了，把这个文件内容转化为json格式后提取mid、id两个参数，再以此构造歌词文件的Request url，就可以拿到所有的歌词了。

综上，整个爬虫分为4个部分：
1.	从文件中提取各首歌的mid、musicid两个参数
2.	构造歌词文件的url，并请求文件内容
3.	清理文件内容，获取歌词并写入txt文件
4.	分词并创建词云图

