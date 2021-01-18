<template>
    <div>
        <!-- 面包屑 -->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/welcome' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>用户管理</el-breadcrumb-item>
        </el-breadcrumb>

        <!-- 分割线 -->
        <el-divider>
        </el-divider>

        <!-- 搜索栏 新建按钮-->
        <el-form class="user-search" :inline="true" label-width="90px">
            <el-form-item prop="user" label="用户账号: ">
                <el-input v-model="id" placeholder="请输入用户账号" clearable></el-input>
            </el-form-item>
            <el-form-item label="">
                <el-button size="small" type="primary"  icon="iconfont icon-chazhao" class="title" round @click="Search()"> 查询用户 </el-button>
            </el-form-item>
            <el-form-item label="">
                <el-button size="small" type="primary" icon="iconfont icon-tianjiaxindeyangbenhe" round @click="handleEdit()"> 新增用户 </el-button>
            </el-form-item>
        </el-form>

        <!-- 列表 -->
        <el-table :data="tempList":fit="true" :show-header="true"
                  :default-sort = "{prop: 'id', order: 'descending'}" :border="true" max-height="430" v-loading = "loading">
            <el-table-column prop="id" label="用户账号" align="center">
            </el-table-column>
            <el-table-column prop="password" label="用户密码" align="center" v-if="false">
            </el-table-column>
            <el-table-column prop="name" label="用户名称" align="center">
            </el-table-column>
            <el-table-column label="操作" fixed="right" align="center" width="200px">
                <template slot-scope="scope">
                    <el-button mc-type="column-el-button" size="mini" type="success" @click="handleEdit(scope.row)">编辑</el-button>
                    <el-button mc-type="column-el-button" size="mini" type="danger" @click="deleteUser(scope.row)">删除</el-button>
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

        <!-- 新建界面 -->
        <el-dialog title="新增用户" :visible.sync="NewFormVisible" width="30%">
            <el-form ref="NewFormRef" label-width="80px" :model="NewForm" :rules="NewRules" >
                <el-form-item label="用户账号" prop="id"  required>
                    <el-input size="small" v-model="NewForm.id" auto-complete="off" prefix-icon="iconfont icon-denglu" placeholder="请输入用户账号"></el-input>
                </el-form-item>
                <el-form-item label="用户密码" prop="password"  required>
                    <el-input size="small" v-model="NewForm.password" auto-complete="off" prefix-icon="iconfont icon-mima" placeholder="请输入用户密码" type="password" show-password></el-input>
                </el-form-item>
                <el-form-item label="用户名称" prop="name"  required>
                    <el-input size="small" v-model="NewForm.name" prefix-icon="iconfont icon-mendian" placeholder="请输入用户名称"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button size="small" @click='NewFormVisible = false'>取消</el-button>
                <el-button size="small" type="primary"  class="title" @click="newForm()">保存</el-button>
            </div>
        </el-dialog>

        <!-- 修改界面 -->
        <el-dialog title="编辑用户" :visible.sync="ModifyFormVisible" width="30%">
            <el-form ref="ModifyFormRef" label-width="80px" :model="ModifyForm" :rules="ModifyRules" >
                <el-form-item label="用户密码" prop="password"  required>
                    <el-input size="small" v-model="ModifyForm.password" auto-complete="off" prefix-icon="iconfont icon-mima" placeholder="请输入用户密码" type="password" show-password></el-input>
                </el-form-item>
                <el-form-item label="用户名称" prop="name"  required>
                    <el-input size="small" v-model="ModifyForm.name" prefix-icon="iconfont icon-mendian" placeholder="请输入用户名称"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button size="small" @click='ModifyFormVisible = false'>取消</el-button>
                <el-button size="small" type="primary"  class="title" @click="modifyForm()">保存</el-button>
            </div>
        </el-dialog>
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
                NewFormVisible:false,   // 控制新建页面显示与隐藏
                ModifyFormVisible:false,   // 控制修改页面显示与隐藏
                totalSize: 20,

                /* 分页 */
                pageSize:10,
                currentPage:1,
                tempList: [],   // 分页数据

                /* 暂时填充用户列表 */
                UserList:
                    [
                        {
                            id: 'halo7',
                            password: '7777777',
                            name: '福建',
                        },
                    ],

                /* 新建页面样式 */
                NewForm: {
                    id: '',
                    password: '',
                    name: '',
                },

                /* 新建表单验证 */
                NewRules: {
                    id: [
                        { required: true, message: '请输入用户账号', trigger: 'blur' },
                        { required: true, message: '请输入用户账号', trigger: 'change' },
                    ],
                    password: [
                        { required: true, message: '请输入用户密码', trigger: 'blur' },
                        { required: true, message: '请输入用户密码', trigger: 'change' },
                    ],
                    name: [
                        { required: true, message: '请输入用户名称', trigger: 'blur' },
                        { required: true, message: '请输入用户名称', trigger: 'change' },
                    ],
                },
                /* 编辑页面样式 */
                ModifyForm: {
                    id: '',
                    password: '',
                    name: '',
                },

                /* 编辑表单验证 */
                ModifyRules: {
                    password: [
                        { required: true, message: '请输入用户密码', trigger: 'blur' },
                        { required: true, message: '请输入用户密码', trigger: 'change' },
                    ],
                    name: [
                        { required: true, message: '请输入用户名称', trigger: 'blur' },
                        { required: true, message: '请输入用户名称', trigger: 'change' },
                    ],
                },
            }
        },

        /* 初始化 */
        created() {
            this.getList();
        },

        methods: {

            /* 获得列表 */
            async getList() {
                this.loading = true;

                const {data: res} = await this.$http.get("/SearchUser", {params:{id: this.id}});

                //设置列表数据
                this.UserList = res.UserList;

                this.loading = false;
                this.totalSize = this.UserList.length;   // 更新总条数
                this.handleSizeChange(this.pageSize);   // 更新分页 界面
            },

            /* 查询 */
            Search()
            {
                this.getList();
                this.totalSize = this.UserList.length;   // 更新总条数
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
                    if (this.UserList[from])
                    {
                        this.tempList.push(this.UserList[from]);
                    }
                }
            },

            /* 显示 新建，编辑 界面 */
            handleEdit: function(row)
            {

                if (row !== undefined && row !== 'undefined')
                {
                    this.ModifyFormVisible = true;
                    this.ModifyForm.id = row.id;
                    this.ModifyForm.password = row.password;
                    this.ModifyForm.name = row.name;
                }
                else
                {
                    this.NewFormVisible = true;
                    this.NewForm.id = '';
                    this.NewForm.password = '';
                    this.NewForm.name = '';
                }

            },

            // 新建 方法
            newForm() {
                this.$refs.NewFormRef.validate(async valid => {
                    if (valid) {
                        const {data:res} = await this.$http.post("/UserNew", this.NewForm);
                        if (res.errmsg === "ok")
                        {
                            await this.getList();
                            this.$message({
                                type: 'success',
                                message: '新建用户成功'
                            })
                            this.NewFormVisible = false
                        }
                        else
                        {
                            this.$message.error('新建失败，用户账号已存在');
                        }
                    }
                    else
                    {
                        return false
                    }
                })
            },

            // 编辑 方法
            modifyForm() {
                this.$refs.ModifyFormRef.validate(async valid => {
                    if (valid) {
                        const {data:res} = await this.$http.put("/UserEdit", this.ModifyForm);
                        if (res.errmsg === "ok")
                        {
                            await this.getList();
                            this.$message({
                                type: 'success',
                                message: '修改用户成功'
                            })
                            this.ModifyFormVisible = false
                        }
                        else
                        {
                            this.$message.error('修改用户失败');
                        }

                    }
                    else
                    {
                        return false
                    }
                })
            },

            // 删除用户
            deleteUser(row) {
                this.$confirm('确定要删除此用户吗?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                })
                .then(async () => {
                    // 删除
                    const {data:res} = await this.$http.delete("/UserDelete", {data: row.id});
                    if (res.errmsg === 'ok')
                    {
                        this.$message({
                            type: 'success',
                            message: '用户已删除'
                        })
                        await this.getList();
                    }
                    else
                    {
                        this.$message({
                            type: 'info',
                            message: "删除失败"
                        })
                    }
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    })
                })
                .catch(err => {
                    console.log(err)
                    this.$message.error('用户删除失败')
                })
            },
        }
    }
</script>

<style lang="less" scoped>

</style>