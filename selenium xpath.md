# **Python Selenium XPath**

## **一 父子、兄弟、相邻节点定位方式详解**

### **1. 由父节点定位子节点**

```
<html>
<body>
<div id="A">
    <!--父节点定位子节点-->
    <div id="B">
        <div>parent to child</div>
    </div>
</div>
</body>
</html>
```
想要根据 B节点 定位无id的子节点，代码示例如下：

```
# -*- coding: utf-8 -*-
from selenium import webdriver

driver = webdriver.Firefox()
driver.get('D:\\py\\AutoTestFramework\\src\\others\\test.html')

# 1.串联寻找
print driver.find_element_by_id('B').find_element_by_tag_name('div').text

# 2.xpath父子关系寻找
print driver.find_element_by_xpath("//div[@id='B']/div").text

# 3.css selector父子关系寻找
print driver.find_element_by_css_selector('div#B>div').text

# 4.css selector nth-child
print driver.find_element_by_css_selector('div#B div:nth-child(1)').text

# 5.css selector nth-of-type
print driver.find_element_by_css_selector('div#B div:nth-of-type(1)').text

# 6.xpath轴 child
print driver.find_element_by_xpath("//div[@id='B']/child::div").text

driver.quit()
```

### **2. 由子节点定位父节点**

```
<html>
<body>
<div id="A">
    <!--子节点定位父节点-->
    <div>
        <div>child to parent
            <div>
                <div id="C"></div>
            </div>
        </div>
    </div>
</div>
</body>
</html>
```


我们想要由 C节点 定位其两层父节点的div，示例代码如下：

```
# -*- coding: utf-8 -*-
from selenium import webdriver

driver = webdriver.Firefox()
driver.get('D:\\py\\AutoTestFramework\\src\\others\\test.html')

# 1.xpath: `.`代表当前节点; '..'代表父节点
print driver.find_element_by_xpath("//div[@id='C']/../..").text

# 2.xpath轴 parent
print driver.find_element_by_xpath("//div[@id='C']/parent::*/parent::div").text

driver.quit()
```

### **3. 由弟弟节点定位哥哥节点**

```
<html>
<body>
<div>
    <!--下面两个节点用于兄弟节点定位-->
    <div>brother 1</div>
    <div id="D"></div>
    <div>brother 2</div>
</div>
</body>
</html>
```

怎么通过 D节点 定位其哥哥节点呢？看代码示例：
```
# -*- coding: utf-8 -*-
from selenium import webdriver

driver = webdriver.Firefox()
driver.get('D:\\Code\\py\\AutoTestFramework\\src\\others\\test.html')

# 1.xpath,通过父节点获取其哥哥节点
print driver.find_element_by_xpath("//div[@id='D']/../div[1]").text

# 2.xpath轴 preceding-sibling
print driver.find_element_by_xpath("//div[@id='D']/preceding-sibling::div[1]").text

driver.quit()
```

### **4. 由哥哥节点定位弟弟节点**
```
# -*- coding: utf-8 -*-
from selenium import webdriver

driver = webdriver.Firefox()
driver.get('D:\\Code\\py\\AutoTestFramework\\src\\others\\test.html')

# 1.xpath，通过父节点获取其弟弟节点
print driver.find_element_by_xpath("//div[@id='D']/../div[3]").text

# 2.xpath轴 following-sibling
print driver.find_element_by_xpath("//div[@id='D']/following-sibling::div[1]").text

# 3.xpath轴 following
print driver.find_element_by_xpath("//div[@id='D']/following::*").text

# 4.css selector +
print driver.find_element_by_css_selector('div#D + div').text

# 5.css selector ~
print driver.find_element_by_css_selector('div#D ~ div').text

driver.quit()
```

## **二 starts-with contains text() not()**
starts-with 顾名思义，匹配一个属性开始位置的关键字
```
# 查找name属性中开始位置包含'name1'关键字的页面元素
//input[starts-with(@name,'name1')]
```
contains 匹配一个属性值中包含的字符串
```
# 查找name属性中包含na关键字的页面元素
//input[contains(@name,'na')]
```
text() 匹配的是显示文本信息，此处也可以用来做定位用
```
<a href="http://www.baidu.com">百度搜索</a>
```
```
//a[text()='百度搜索'] 
```
```
//a[contains(text(),"百度搜索")]
```
not()函数，表示否定
```
# 匹配出name为identity并且class的值中不包含a的input节点
//input[@name='identity' and not(contains(@class,'a'))]
```