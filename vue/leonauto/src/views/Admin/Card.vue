<template>
    <div>
        <!-- 面包屑 -->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>功能管理</el-breadcrumb-item>
            <el-breadcrumb-item>自动打卡</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 分割线 -->
        <el-divider>
        </el-divider>

        <!-- 搜索栏 新建按钮-->
        <el-form class="user-search" :inline="true" label-width="90px">
            <el-form-item prop="username" label="用户账号: ">
                <el-input v-model="id" placeholder="请输入用户账号" clearable></el-input>
            </el-form-item>
            <el-form-item label="">
                <el-button size="small" type="primary"  icon="iconfont icon-chazhao" class="title" round @click="Search()"> 查询用户 </el-button>
            </el-form-item>
        </el-form>

        <!-- 列表 -->
        <el-table :data="tempList" :fit="true" :show-header="true"
                  :default-sort = "{prop: 'id', order: 'descending'}" :border="true" max-height="430" v-loading = "loading">
            <el-table-column prop="id" label="用户账号" align="center">
            </el-table-column>
            <el-table-column prop="email" label="用户邮箱" align="center">
            </el-table-column>
            <el-table-column prop="CardOn" label="打卡功能" align="center">
            <template slot-scope="scope">
            <el-switch
                v-model="scope.row.CardOn"
                active-color="#13ce66"
                active-text='开'
                inactive-color="#ff4949"
                inactive-text='关'>
            </el-switch>
            </template>
            </el-table-column>
            <el-table-column prop="EmailOn" label="邮件提醒功能" align="center">
            <template slot-scope="scope">
            <el-switch
                v-model="scope.row.EmailOn"
                active-color="#13ce66"
                active-text='开'
                inactive-color="#ff4949"
                inactive-text='关'>
            </el-switch>
            </template>
            </el-table-column>
            <el-table-column label="操作" fixed="right" align="center" width="200px">
                <template slot-scope="scope">
                    <el-button mc-type="column-el-button" size="mini" type="success" @click="SaveCard(scope.row)">保存此状态</el-button>
                </template>
            </el-table-column>
        </el-table>

        <br/>
        <br/>

        <!-- 分页 -->
        <div class="block" align="center">
            <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[10, 15, 20, 25]"
                    :page-size="pageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total= totalSize>
            </el-pagination>
        </div>
    </div>
</template>

<script>
    export default
    {
        data()
        {
            return{

                loading: false,   // 加载中
                id:'',   // 搜索框 用户ID
                totalSize: 20,

                /* 分页 */
                pageSize:10,
                currentPage:1,
                tempList: [],   // 分页数据

                /* 暂时填充用户列表 */
                CardList:
                    [],
            }
        },

        /* 初始化 */
        created() {
            this.getList();
        },

        watch:{

        },

        methods: {

            /* 获得列表 */
            async getList() {
                this.loading = true;

                const {data: res} = await this.$http.get("/SearchCard", {params:{id: this.id}});
                
                //设置列表数据
                this.CardList = res.CardList;

                this.loading = false;
                this.totalSize = this.CardList.length;   // 更新总条数
                this.handleSizeChange(this.pageSize);   // 更新分页 界面
            },

            /* 查询 */
            Search()
            {
                this.getList();
                this.totalSize = this.CardList.length;   // 更新总条数
                this.handleSizeChange(this.pageSize);   // 更新分页 界面
            },

            /* 分页更新功能 */
            handleSizeChange(val)
            {
                this.pageSize = val;
                this.handleCurrentChange(this.currentPage);
            },

            /* 分页与排序不可兼得 */
            handleCurrentChange(val)
            {
                this.currentPage = val;
                let from = (this.currentPage - 1) * this.pageSize;
                let to = this.currentPage * this.pageSize;
                this.tempList = [];
                for (; from < to; from++)
                {
                    if (this.CardList[from])
                    {
                        this.tempList.push(this.CardList[from]);
                    }
                }
            },


            async SaveCard(row)
            {
                const {data:res} = await this.$http.post("/SaveCard", {id: row.id, CardOn: row.CardOn, EmailOn: row.EmailOn});
                if(res && res.errmsg ===  'ok')
                {
                    this.$message({
                        type: 'success',
                        message: '保存成功'
                    })
                }
                else if(res && res.errmsg === 'logic_error')
                {
                    this.$message.error('关闭打卡功能情况下，不能打开邮件提醒功能');
                    this.getList();
                }
                else
                {
                    this.$message.error('保存失败');
                    this.getList();
                }
            },
        }
    }
</script>

<style lang="less" scoped>

</style>