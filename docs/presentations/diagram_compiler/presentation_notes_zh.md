# Diagram Compiler 介绍讲稿

## 1. 开场
这不是把一个黑箱模型接到 Monte Carlo 上，而是先把固定阶图的物理语义写成显式 DiagramIR，再沿着同一份语义生成不同执行路径。当前交付是 experimental research preview，验证到 LEVEL 2，生产 P1 没有被替换。

## 2. 理论背景
电子声子问题的图展开由电子传播子、声子传播子、顶点和整体归一化组成。固定阶时，所有配对图共享大量中间表达式；两带问题还要保持矩阵乘法顺序。计算瓶颈因此同时来自图数量和每张图内部的矩阵工作。

## 3. 核心原理
DiagramIR 把 family、配对、因子、动量形式和 binding contract 分开。Exact DAG 保留完整图表达；cheap DAG 使用版本化 `propagator_only_v1`，只产生状态权重。两者都来自同一份 IR，避免手工复制物理公式。

## 4. 延迟接受
Stage 1 用 cheap state weight 做早拒绝。通过后才算 exact target。Stage 2 使用 `ell_R - ell_hat` 修正 cheap 近似和 Hastings ratio，因此在 `positive_real_F_v1` 的支持域内保持目标分布。这里的证据是有限状态 balance/stationarity 和 mutation falsifiers。

## 5. 编译链
NativeKernelIR 明确记录类型、SSA、CFG、ABI、status 和 exact region。Fortran backend 只消费 NativeKernelIR，不再理解 DiagramIR 或 DA 数学。Task 6 用固定 Ubuntu 22.04/gfortran 11.4 Docker 环境编译同一生成源码，并与 NativeKernelIR interpreter 对比。

## 6. 数据怎么读
图表中的 224/224、最大误差、primitive error、exact laziness、balance residual 都来自仓库 CSV/JSON。节点数是结构证据，不等于 wall-clock speedup。当前没有声称 Monte Carlo 加速。

## 7. 真实材料接入
真实材料路径是 QE/DFPT 和 Wannier/Perturbo 提供能带、声子频率和电子声子耦合，再由 provider adapter 映射到 BindingLayout。真正进入 compiler 前，还需要单位、规范、矩阵基、measure、Jacobian、reverse proposal 和独立 oracle 全部闭合。Task 6 的 synthetic two-band kernel 还不能算真实材料接入。

## 8. 能解决什么问题
当前可以解决固定阶图表达不透明、exact/cheap 路径重复实现、native lowering 缺少可追溯契约的问题。下一层科学问题是：在真实材料完整 observable 上，能否保持同一物理和误差合同，并在同精度下证明总成本下降。

## 9. 收尾
最稳妥的定位是：bounded physics-aware diagram compiler。它是计算方法和软件方法创新，创新点在显式物理 IR、exact-preserving DA、typed native lowering 和可复现验证链；不是通用 QFT compiler，也不是生产 FEP-DMC replacement。
