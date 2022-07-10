## 【过程记录】MultiLevel L-system

### 2022/7/10

今天是近乎摆烂的一天……但也不是一无所获。

[乔布·塔勒 |林登迈尔系统 (jobtalle.com)](https://jobtalle.com/lindenmayer_systems.html)

又发现一位巨佬的Lsystem实现。文章讲得也很系统，后面也有包括植物分布、生态系统的的其他文章。

现在当务之急还是先做好一个basic的3D L-system

就让我来缕一缕到底需要什么东西。

用L-system绘制一棵树有两步

1.  规则生成
2.  绘制

第一步就是纯纯地生成一串L-system的文本。第二步就是用模型去实现文本的语义描述。

