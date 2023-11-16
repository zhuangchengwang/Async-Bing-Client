# Part 1
## 项目规范
- 使用gorm作为orm层
- 一个完整的接口至少包括 api层,service层,model层,requet层,routers层,response层 6个层级
- curd操作请学习并模仿下方代码示例的分层写法
## 业务概念
- 达人: 一个用户会关联多个达人,用户id是user_id,达人id是author_id,两者不相同,是一对多的概念
## 常用方法

### 获取蝉选数据库gorm.DB实例
```golang
  // global.JX_DB 如下:
  err = global.JX_DB.Create(banner).Error
```

## 代码示例
### ddl
### model层
文件:`model/jxdata/jx_good_banner_model.go`
```golang
package jxdata
import (
	"adminserver/global"
	"adminserver/model/jxdata/constant"
	"time"
)
// JxGoodBanner 商品栏目
type JxGoodBanner struct {
	ID           int       `gorm:"primaryKey;column:id;type:int(11);not null" json:"id"`
	Name         string    `gorm:"column:name;type:varchar(255);not null;default:''" json:"name"` // 栏目名称
	Desc         string    `gorm:"column:desc;type:varchar(1000);not null" json:"desc"`           // 简介
	Status       int       `gorm:"column:status;type:int(11);not null;default:0" json:"status"`   // 状态 1未启用   2启用
	Sort         int       `gorm:"column:sort;type:int(11);not null;default:0" json:"sort"`                   // 排序
    CreatedAt    time.Time `gorm:"column:created_at;type:datetime"`
	UpdatedAt    time.Time `gorm:"column:updated_at;type:datetime"`
}
// 创造对象
func NewJxGoodBanner() *JxGoodBanner {
	return new(JxGoodBanner)
}
// 增加一条记录,不验证数据格式,由service层验证
func (m *JxGoodBanner) Add(banner *jxdata.JxGoodBanner) (err error) {
	err = global.JX_DB.Create(banner).Error
	return
}
// 获取所有启用的专题列表-sort 升序
func (m *JxGoodBanner) GetEnableAllBannerList() (lst []*JxGoodBanner, err error) {
	lst = make([]*JxGoodBanner, 0)
	err = global.JX_DB.Where("status = ?", constant.JxGoodBannerStatusEnable).Order("sort asc").Find(&lst).Error
	return
}
```
### service层
文件:`service/jingxuan/jx_good_banner_service.go`
```golang
package jingxuan

import (
	"adminserver/global"
	"adminserver/model/jxdata"
	"adminserver/model/jxdata/request"
    "adminserver/model/jxdata/response"
)

type JxGoodBannerService struct {
}

func NewJxGoodBannerService() *JxGoodBannerService {
	return new(JxGoodBannerService)
}
// 添加栏目
func (service *JxGoodBannerService) Add(bannerReq *request.AddBannerReq) (err error) {
    banner := new(jxdata.JxGoodBanner)
    banner.Name = bannerReq.Name
    banner.Desc = bannerReq.Desc
    banner.Status = 1
    err = jxdata.NewJxGoodBanner().Add(banner)
	return
}

// 获取栏目映射 id->name
func (service *JxGoodBannerService) GetBannerMap() (res map[int]*response.Info, err error) {
	lst, err := jxdata.NewJxGoodBanner().GetEnableAllBannerList()
	if err != nil {
		return
	}
	res = make(map[int]string, 0)
	for _, item := range lst {
        info := new(response.Info)
        info.Name = item.Name			
        info.Msg = fmt.Sprintf("%v很不错!",item.Name)
		// 转化成 model.Time的格式
		info.CreatedAt = model.Time(item.CreatedAt)
		res[item.ID] = info
	}
	return
}
```

### request层
文件:`model/jxdata/request/jx_good_banner_request.go`
```golang
package request
type AddBannerReq struct {
	Name         string `json:"name" form:"name" validate:"required"`
	Desc         string `json:"desc" form:"desc" validate:"required"`
}
```
### response层
文件:`model/jxdata/response/jx_good_banner_reponse.go`
```golang
import "adminserver/model"
type Info struct {
	Name        string `json:"name"`
	Msg         string `json:"msg"`
	CreatedAt   model.Time `json:"created_at"` // 使用model.Time时间类型,json解析后的格式对人友好
}
```
### api层
文件:`api/v1/jingxuan/jx_good_banner_api.go`
```golang
package jingxuan

import (
	"adminserver/model/jxdata/response"
	"adminserver/model/jxdata/request"
	"adminserver/service/jingxuan"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/gookit/validate"
)

type JxGoodBannerApi struct {
}

func (*JxGoodBannerApi) Add(c *gin.Context) {
	var req request.AddBannerReq
	err := c.ShouldBindJSON(&req)
	if err != nil {
		response.FailWithMessage(fmt.Sprintf("%+v", err), c)
		return
	}
    // 验证请求参数
	vv := validate.Struct(req)
	if !vv.Validate() {
		response.FailWithMessage(fmt.Sprintf("%+v", vv.Errors.One()), c)
		return
	}
	err = jingxuan.NewJxGoodBannerService().Add(req)
	if err != nil {
		response.FailWithMessage(err.Error(), c)
	} else {
		response.OkWithDetailed("", "添加成功", c)
	}
}

func (*JxGoodBannerApi) GetBannerMap(c *gin.Context) {
	data, err := jingxuan.NewJxGoodBannerService().GetBannerMap()
	if err != nil {
		response.FailWithMessage(err.Error(), c)
		return
	}
	response.OkWithDetailed(data,"操作成功", c)
}
```

### routers层
文件:`router/jingxuan/jx_good_banner_router.go`
```golang
package jingxuan
import (
	v1 "adminserver/api/v1"

	"github.com/gin-gonic/gin"
)
type JxGoodBannerRouter struct {
}
func (rec *JxGoodBannerRouter) InitJxGoodBannerRouter(Router *gin.RouterGroup) {
	router := Router.Group("banner")
	var api = v1.ApiGroupApp.JxApiGroup.JxGoodBannerApi
	{
		router.GET("get-banner-map", api.GetBannerMap)
		router.POST("add", api.Add)
	}
}
```
# Part 2
## 额外方法

## 已完成的代码
### ddl
```sql
create table jx_dk_user_maintain
(
    id                int auto_increment
        primary key,
    user_id           int          null comment '抖客用户id(也是蝉选用户)',
    operator_uuid     varchar(30)  null comment '操作者uuid(运营人员)',
    operator_nickname varchar(32)  null comment '操作昵称',
    type              int          null comment '评论类型;1:添加未通过;2:添加已通过;3:下滑已沟通;4其他',
    comment           varchar(100) null comment '评论',
    created_at        datetime     null
)
    comment '抖客用户维护';
```
------------
请仔细阅读并理解上面 <Part 1> 和 <Part 2>的内容, 实现下面的需求:
# 需求
- 判断下<Part 2>的<额外方法>是否提供有效的内容,如果是,请思考如何调用<Part 2>的<额外方法>实现下面相关的功能
- 判断下<Part 2>的<已完成的代码>是否提供有效的内容,如果是,请思考如何从<Part 2>的<已完成的代码>后面,继续编写其他层级的代码

- 功能:1.实现列表接口,获取某个user_id的所有评论信息,按时间倒序;2.生成评论接口;3.删除某条评论接口


- 仔细理解<Part 1>的<项目规范>,<业务概念>,<常用方法>,以及<代码示例>里面的注释内容,思考如何按照<Part 1>的<项目规范>实现代码
- 现在开始,我认为你已经准备就绪,接下来请为我生成request层的代码,格式需要和<代码示例>中保持一致;
- 以"### request层\n"开头,编写代码
- golang代码需用"```golang <golang代码>```" markdown可解析的格式输出