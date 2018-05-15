# -*- coding: utf-8 -*-

# @File    : index.py
# @Date    : 2018-05-10
# @Author  : 彭世瑜

# 使用flask创建一个导航主页管理

from flask import Flask, render_template, request, url_for, redirect
from model import ClassifyModel
from model import WebsiteModel
from spider import get_website_info

app = Flask(__name__)

# 首页
@app.route("/")
def index():
    websites = WebsiteModel.select()
    classifies = ClassifyModel.select()
    dct = {
        "websites": websites,
        "classifies": classifies
    }
    return render_template("index.html", **dct)

# 管理首页
@app.route("/admin")
def admin():
    websites = WebsiteModel.select().order_by(-WebsiteModel.weight)
    return render_template("admin.html", websites=websites)

# 删除
@app.route("/delete")
def delete():
    uid = request.args.get("uid")
    WebsiteModel.delete().where(WebsiteModel.id==uid).execute()
    return redirect(url_for("admin"))

# 编辑, 新增和修改
@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method=="GET":
        uid = request.args.get("uid")
        website = WebsiteModel.select().where(WebsiteModel.id==uid).first()
        classifies = ClassifyModel.select()

        return render_template("edit.html", website=website, classifies=classifies)


    elif request.method == "POST":

        title = request.form.get("title")
        if title == "": return "网站名称不能为空！"

        url = request.form.get("url")
        if url == "": return "网站链接不能为空！"

        ico = request.form.get("ico")
        print("ico", type(ico), ico)

        ret = None
        if ico == "":
            ret = get_website_info(url)
            ico = ret.get("icon")
        description = request.form.get("description")
        if description=="":
            if ret ==None:
                ret = get_website_info(url)
            description =ret.get("title")

        classify_id = request.form.get("classify")
        print(classify_id, type(classify_id))
        classify_id = 0 if classify_id=="" else int(classify_id)
        weight = request.form.get("weight")
        weight = 0 if weight=="" else int(weight)

        uid = request.form.get("uid")
        if uid !="":
            ret = WebsiteModel.select().where(WebsiteModel.id==uid).first()
        else:
            ret = None

        # 存在则更新
        if ret:
            print("更新")
            WebsiteModel.update(
                title=title,
                ico=ico,
                description=description,
                url=url,
                classify_id=classify_id,
                weight=weight
            ).where(WebsiteModel.id==uid).execute()

        # 不存在则添加数据
        else:
            print("添加")
            WebsiteModel.create(
                title=title,
                ico=ico,
                description=description,
                url=url,
                classify_id=classify_id,
                weight=weight
            )

        return redirect(url_for("admin"))


# 编辑分类, 新增和修改
@app.route("/classify", methods=["GET", "POST"])
def classify():
    if request.method=="GET":
        classifies = ClassifyModel.select()
        return render_template("classify.html", classifies=classifies)

    elif request.method=="POST":
        name = request.form.get("name")
        ClassifyModel.create(name=name)
        return redirect(url_for("classify"))

# 删除标签分类
@app.route("/delete-classify")
def delete_classify():
    uid = request.args.get("uid")
    classify = ClassifyModel.select().where(ClassifyModel.id == uid).first()

    if len(classify.websites)==0:  # 有内容的分类不能删除
        ClassifyModel.delete().where(ClassifyModel.id == uid).execute()
    else:
        print("有内容的分类不能删除")
    return redirect(url_for("classify"))


if __name__ == "__main__":
    app.run()