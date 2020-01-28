
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from matplotlib.font_manager import FontProperties

fp = FontProperties(fname=r'C:\Windows\Fonts\YUMIN.TTF', size=8)

# GOTHICI.TTF YUMIN.TTF
df = pd.read_csv('join.csv',encoding='cp932')
df = df[df['runnerName'] == '安部智晴']

#df.drop(columns=['elapsedRank','elapsedTime','legSpeed','legLossTime','lapRank','lapTime','from'],inplace=True)
df.drop_duplicates(inplace=True)

class GaussianMixture(object):

    def __init__(self, n_component):
        # ガウス分布の個数
        self.n_component = n_component

    # EMアルゴリズムを用いた最尤推定
    def fit(self, X, iter_max=10):
        # データの次元
        self.ndim = 1
        # 混合係数の初期化
        self.weights = np.ones(self.n_component) / self.n_component
        # 平均の初期化
        self.means = np.random.uniform(X.min(), X.max(), (self.ndim, self.n_component))
        # 共分散行列の初期化
        self.covs = np.repeat(10 * np.eye(self.ndim), self.n_component).reshape(self.ndim, self.ndim, self.n_component)

        # EステップとMステップを繰り返す
        for i in range(iter_max):
            params = np.hstack((self.weights.ravel(), self.means.ravel(), self.covs.ravel()))
            # Eステップ、負担率を計算
            resps = self.expectation(X)
            # Mステップ、パラメータを更新
            self.maximization(X, resps)
            # パラメータが収束したかを確認
            if np.allclose(params, np.hstack((self.weights.ravel(), self.means.ravel(), self.covs.ravel()))):
                break
        else:
            print("parameters may not have converged")

    # ガウス関数
    def gauss(self, X):
        precisions = np.linalg.inv(self.covs.T).T
        diffs = X[:, :, None] - self.means
        assert diffs.shape == (len(X), self.ndim, self.n_component)
        exponents = np.sum(np.einsum('nik,ijk->njk', diffs, precisions) * diffs, axis=1)
        assert exponents.shape == (len(X), self.n_component)
        return np.exp(-0.5 * exponents) / np.sqrt(np.linalg.det(self.covs.T).T * (2 * np.pi) ** self.ndim)

    # Eステップ
    def expectation(self, X):
        # PRML式(9.23)
        resps = self.weights * self.gauss(X)
        resps /= resps.sum(axis=-1, keepdims=True)
        return resps

    # Mステップ
    def maximization(self, X, resps):
        # PRML式(9.27)
        Nk = np.sum(resps, axis=0)

        # PRML式(9.26)
        self.weights = Nk / len(X)

        # PRML式(9.24)
        self.means = X.T.dot(resps) / Nk

        diffs = X[:, :, None] - self.means
        # PRML式(9.25)
        self.covs = np.einsum('nik,njk->ijk', diffs, diffs * np.expand_dims(resps, 1)) / Nk

    # 確率分布p(x)を計算
    def predict_proba(self, X):
        # PRML式(9.7)
        gauss = self.weights * self.gauss(X)
        return np.sum(gauss, axis=-1)

    # クラスタリング
    def classify(self, X):
        joint_prob = self.weights * self.gauss(X)
        return np.argmax(joint_prob, axis=1)


x = df['legSpeed'].sort_values().values

model = GaussianMixture(3)
model.fit(x,iter_max=100)


probs = model.predict_proba(x)

plt.plot(x,probs)
plt.show()