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
    CreatedAt    model.Time `gorm:"column:created_at;type:datetime"`
	UpdatedAt    model.Time `gorm:"column:updated_at;type:datetime"`
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
type Info struct {
	Name         string `json:"name"`
	Msg         string `json:"msg"`
}
```
### api层
文件:`api/v1/jingxuan/jx_good_banner_api.go`
```golang
package jingxuan

import (
	"adminserver/model/common/response"
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
func (rec *JxGoodBannerRouter) InitRouter(Router *gin.RouterGroup) {
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
create table jx_activity_promotion
(
    id              int auto_increment comment '自增 id'
        primary key,
    period tinyint (3) default 0 not null comment '活动的期数',
    dy_id           int         default 0  not null comment '抖音 id',
    user_id         int         default 0  not null comment '蝉选用户 id',
    author_id       varchar(32) default '' not null comment '达人 id',
    author_info     json                   null comment '达人信息（带货等级、头像、粉丝等信息）',
    team_name       varchar(64) default '' not null comment '团队名称（or 个人）',
    user_name       varchar(64) default '' not null comment '用户名称',
    mobile          varchar(32) default '' not null comment '联系电话',
    region          tinyint(3)  default 0  not null comment '赛区 1-新人成长赛 2-达人冲刺赛 3-大神擂台赛 4-团队赛区',
    type            tinyint(3)  default 0  not null comment '参赛类型 1-个人 2-团队',
    race_no         varchar(32) default '' not null comment '参赛编号（同个团队的编号相同）',
    is_leader       tinyint(3)  default 0  not null comment '是否是团长 1-是 0-否',
    is_new          tinyint(3)  default 0  not null comment '是否是新用户 1-是 0-否',
    order_count     int         default 0  not null comment '订单数',
    total_gmv       int         default 0  not null comment '全站 gmv',
    settlement_gmv  int         default 0  not null comment '结算 gmv',
    payment_gmv     int         default 0  not null comment '支付gmv',
    service_fee     int         default 0  not null comment '结算服务费',
    participated_at datetime               null comment '参加时间',
    del_flag        tinyint(3)  default 0  not null comment '资格标记 1-已经删除 0-未删除',
    created_at      datetime               null comment '创建时间',
    updated_at      datetime               null comment '更新时间',
    constraint dy_id
        unique (dy_id, region, del_flag)
)
    comment '蝉选晋级赛活动报名表';
```
------------
请仔细阅读并理解上面 <Part 1> 和 <Part 2>的内容, 实现下面的需求:
# 需求
- 判断下<Part 2>的<额外方法>是否提供有效的内容,如果是,请思考如何调用<Part 2>的<额外方法>实现下面相关的功能
- 判断下<Part 2>的<已完成的代码>是否提供有效的内容,如果是,请思考如何从<Part 2>的<已完成的代码>后面,继续编写其他层级的代码

- 功能:实现列表接口,根据活动期数,用户id,团队名称,手机号,报名时间 进行搜索,返回列表和其他统计信息;其中列表项包含机构名称,团长用户名,团队联系人,团队名称,团长手机号,报名时间,团队人数,出单人数,结算服务费,支付时间,订单数,结算GMV,支付GMV 等字段;统计信息包含:报名用户数,参赛抖音号数,拉新抖音号数,报名团队数,总订单数,总gmv,出单商品数


- 仔细理解<Part 1>的<项目规范>,<业务概念>,<常用方法>,以及<代码示例>里面的注释内容,思考如何按照<Part 1>的<项目规范>实现代码
- 现在开始,我认为你已经准备就绪,接下来请为我生成request层的代码,格式需要和<代码示例>中保持一致;
- 以"### request层\n"开头,编写代码
- golang代码需用"```golang <golang代码>```" markdown可解析的格式输出