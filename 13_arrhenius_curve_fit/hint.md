# 项目 13 渐进提示

请一次只看一条提示。先独立尝试；只有卡住时，再继续查看下一条。

## 提示 1

先把路径、必需列、缺失值、温度和扩散系数检查完成，再进行拟合。把 CSV 实验观测
数组命名为 `diffusion_measured_m2_s`，再除以 `1.0e-12` 得到
`diffusion_measured_scaled`，作为 `curve_fit()` 的拟合目标。

## 提示 2

Arrhenius 模型函数的第一个参数是 `temperature_k`，后面两个参数是需要拟合的
`prefactor_scaled` 和 `activation_energy_j_mol`。`curve_fit()` 返回的最优参数数组
顺序与模型函数中的参数顺序一致。

## 提示 3

先用最优参数得到 `diffusion_predicted_scaled`，再乘以 `1.0e-12` 得到
`diffusion_predicted_m2_s`。用 `diffusion_measured_m2_s` 减去它即可得到
`residual_m2_s`。绘制平滑曲线时，可以另建一个覆盖最低到最高摄氏温度的递增数组，
换算为开尔文温度后交给同一个模型函数。
