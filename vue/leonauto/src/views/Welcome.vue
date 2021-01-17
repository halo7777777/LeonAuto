<template>
    <div>

        <el-carousel :interval="3000" height="500px"  type=card>
            <el-carousel-item v-for="item in src" :key="item">
                <img :src="item" class="image">
            </el-carousel-item>
        </el-carousel>


    </div>
</template>

<script>
    export default
    {
        data() {
            return {
                src: [
                            "https://pic.downk.cc/item/5f910c1b1cd1bbb86ba90dbf.jpg",
                            "https://pic.downk.cc/item/5f910c1b1cd1bbb86ba90db5.jpg",
                            "https://pic.downk.cc/item/5f910c1a1cd1bbb86ba90da1.jpg",
                            "https://pic.downk.cc/item/5f910c1a1cd1bbb86ba90d95.jpg",
                            "https://pic.downk.cc/item/5f910c1d1cd1bbb86ba90e0a.jpg",
                            "https://pic.downk.cc/item/5f910c241cd1bbb86ba91034.jpg",
                            "https://pic.downk.cc/item/5f910c241cd1bbb86ba9105a.jpg",
                            "https://pic.downk.cc/item/5f910c241cd1bbb86ba9104b.jpg",
                            "https://pic.downk.cc/item/5f910c241cd1bbb86ba91063.jpg",
                            "https://pic.downk.cc/item/5f910c231cd1bbb86ba9101b.jpg",
                            "https://pic.downk.cc/item/5f910c2d1cd1bbb86ba91235.jpg",
                            "https://pic.downk.cc/item/5f910c2c1cd1bbb86ba91208.jpg",
                            "https://pic.downk.cc/item/5f910c2c1cd1bbb86ba9121b.jpg",
                            "https://pic.downk.cc/item/5f910c2c1cd1bbb86ba911ff.jpg",
                            "https://pic.downk.cc/item/5f910c2c1cd1bbb86ba91213.jpg",
                ],
            }
        }
    }
</script>

<style lang="less">
    .el-carousel__item{
        .h3 {
            color: #475669;
            font-size: 14px;
            opacity: 0.75;
            line-height: 200px;
            margin: 0;
        }
        .image{
            width: 700px;
            height: 500px;
            align-content: center;
        }
    }

    .el-carousel__item:nth-child(2n) {
        background-color: #99a9bf;
    }

    .el-carousel__item:nth-child(2n+1) {
        background-color: #d3dce6;
    }
</style>