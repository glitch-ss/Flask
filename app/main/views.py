from datetime import datetime
from flask import render_template,session,redirect,url_for,jsonify,request
import os

from . import main
from .forms import searchForm
from .. import db


print "############################"
temp_Path = os.path.abspath('.')
while os.path.split(temp_Path)[1] != 'flask':
    temp_Path = os.path.split(temp_Path)[0]
temp_Path = os.path.join(temp_Path, "app", "static", "products")
brands=os.listdir(temp_Path)
for brand in brands:
    if brand=="coach":
        coach_brands=os.path.join(temp_Path,brand)
    if brand=="katespade":
        katespade_brands=os.path.join(temp_Path,brand)
        print katespade_brands




def required(x):
    def decorator(f):
    	def wrapper(*args, **kws):
            if x:
            	return f(*args, **kws)
            else:
            	pass
        return wrapper
    return decorator


@main.route('/',methods=['GET','POST'])
def index():
    return render_template('welcome.html')


@main.route('/katespade',methods=['GET','POST'])
@required(katespade_brands)
def katespade():
    x=katespade_brands
    form=searchForm()
    if form.validate_on_submit():
        return redirect(url_for('.index'))
    return render_template('brand_page.html',images=x,form=form,current_time=datetime.utcnow(),brands="katespade")

@main.route('/coach',methods=['GET','POST'],endpoint="goto_coach")
@required(coach_brands)
def coach():
    x=coach_brands
    categories = os.listdir(x)
    bag_name={}
    for category in categories:
        category_Path=os.path.join(x,category)
        coach_bags_name = os.listdir(category_Path)
        bag_name[category]={}
        for coach_bag_name in coach_bags_name:
            bag_file=os.path.join(category_Path, coach_bag_name)
            bags=os.listdir(bag_file)
            if len(bags)==0:
                continue
            bag_name[category][coach_bag_name]=os.path.join('products','coach',category,coach_bag_name,bags[1]).replace('\\','/')
    return render_template('brand_page.html',images=bag_name['Bags'],current_time=datetime.utcnow(),brands="coach")

@main.route('/_add_numbers')
def add_num():
    a=request.args.get('a',0,type=int)
    b=request.args.get('b',0,type=int)
    return jsonify(result=a+b)

@main.route('/<brands>/<category>/<name>',endpoint="gotobags")
@required(temp_Path)
def bags(brands,category,name):
    bag_brand=brands
    bag_name=name
    bag_category=category
    bag_url=os.path.join(temp_Path,brands,bag_category,bag_name)
    print bag_url
    bags_url=os.listdir(bag_url)
    bags_url_list={}
    for bag_list in bags_url:
        color_name_list=bag_list.split('_',1)
        if len(color_name_list)<=1:
            f=open(os.path.join(bag_url,bag_list))
            details=f.read()
            print details
            f.close()
        else:
            color_name=color_name_list[1]
            bag_color=color_name.split('+',1)[0]
            color_number=color_name.split("+",1)[1]
            if bag_color not in bags_url_list.keys():
                bags_url_list[bag_color]=[]
            bags_url_list[bag_color].append(os.path.join('products',bag_brand,category,bag_name,bag_list).replace('\\','/'))
    print bag_color
    return render_template('bag_page.html',bag_brand=bag_brand,bag_name=bag_name,bags_url_list=bags_url_list[bag_color],details=details)
