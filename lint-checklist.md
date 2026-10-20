# lint 检查清单

1. 失效指针（registry/README 引用的路径存在吗）
2. 孤儿页（存在但未登记）
3. registry 与目录树一致
4. frontmatter 最小集齐全（抽查）
5. 机器域 verified_at 超 30 天清单
6. review_needed 超期未裁决
7. log 与实际变更对应（git log 抽查）
8. 镜像与权威一致（如启用镜像层）
