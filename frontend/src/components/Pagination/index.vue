<template>
  <div class="pagination-container">
    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      :page-sizes="[10, 20, 30, 50]"
      layout="total, sizes, prev, pager, next"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script>
export default {
  name: 'Pagination',
  props: {
    total: {
      required: true,
      type: Number
    },
    page: {
      type: Number,
      default: 1
    },
    limit: {
      type: Number,
      default: 10
    }
  },
  emits: ['pagination', 'update:page', 'update:limit'],
  data() {
    return {
      currentPage: this.page,
      pageSize: this.limit
    }
  },
  methods: {
    handleSizeChange(val) {
      this.pageSize = val
      this.$emit('update:limit', val)
      this.$emit('pagination', { page: this.currentPage, limit: val })
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.$emit('update:page', val)
      this.$emit('pagination', { page: val, limit: this.pageSize })
    }
  }
}
</script>

<style scoped>
.pagination-container {
  padding: 32px 16px;
  text-align: right;
}
</style> 