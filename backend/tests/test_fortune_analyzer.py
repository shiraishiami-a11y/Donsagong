"""
吉凶判定サービスのテスト
"""
import pytest
from app.services.fortune_analyzer import FortuneAnalyzer


class TestFortuneAnalyzer:
    """FortuneAnalyzerのテストクラス"""

    @pytest.fixture
    def analyzer(self):
        """テスト用のFortuneAnalyzerインスタンス"""
        return FortuneAnalyzer()

    def test_analyzer_initialization(self, analyzer):
        """初期化テスト"""
        assert analyzer is not None
        assert analyzer.tengan_matrix is not None
        assert analyzer.jiji_matrix is not None
        assert analyzer.johoo_table is not None

    def test_tengan_relation_good(self, analyzer):
        """天干関係（吉）のテスト"""
        # 甲木 → 丙火 = 吉（木生火）
        result = analyzer._check_tengan_relation("甲", "丙")
        assert result in ["吉", "大吉"]

    def test_tengan_relation_bad(self, analyzer):
        """天干関係（凶）のテスト"""
        # 甲木 → 己土 = 大凶（甲己合）
        result = analyzer._check_tengan_relation("甲", "己")
        assert result in ["凶", "大凶"]

    def test_jiji_relation_good(self, analyzer):
        """地支関係（吉）のテスト"""
        # 寅 → 午 = 大吉（寅午戌 三合火局）
        result = analyzer._check_jiji_relation("寅", "午")
        assert result in ["吉", "大吉"]

    def test_jiji_relation_bad(self, analyzer):
        """地支関係（凶）のテスト"""
        # 寅 → 申 = 大凶（寅申沖）
        result = analyzer._check_jiji_relation("寅", "申")
        assert result in ["凶", "大凶"]

    def test_johoo_summer_birth(self, analyzer):
        """調候判定（夏生まれ）のテスト"""
        # 夏（午月）生まれ → 冬（子地支）大運 = 大吉
        result = analyzer._check_johoo("午", "子", "甲")
        assert result in ["吉", "大吉"]

    def test_johoo_winter_birth(self, analyzer):
        """調候判定（冬生まれ）のテスト"""
        # 冬（子月）生まれ → 夏（午地支）大運 = 大吉
        result = analyzer._check_johoo("子", "午", "甲")
        assert result in ["吉", "大吉"]

    def test_special_johoo_ding_fire(self, analyzer):
        """特殊調候（丁火）のテスト"""
        # 丁火日干 → 秋冬調候が吉
        result = analyzer._check_special_johoo("子")  # 冬
        assert result in ["吉", "大吉"]

        result = analyzer._check_special_johoo("午")  # 夏
        assert result == "凶"

    def test_special_johoo_xin_metal(self, analyzer):
        """特殊調候（辛金）のテスト"""
        # 辛金日干 → 秋冬調候が吉
        result = analyzer._check_johoo("午", "子", "辛")  # 辛金は特殊ルール
        assert result in ["吉", "大吉"]

    def test_daeun_fortune_positive(self, analyzer):
        """大運吉凶判定（吉運）のテスト"""
        # 有利な大運の例
        result = analyzer.analyze_daeun_fortune(
            day_stem="甲",
            day_branch="寅",
            hour_stem="丙",
            hour_branch="午",
            month_branch="午",  # 夏生まれ
            daeun_stem="丙",  # 甲→丙 = 吉
            daeun_branch="子",  # 夏生まれ→冬大運 = 大吉（調候）
        )
        assert result in ["吉", "大吉"]

    def test_daeun_fortune_negative(self, analyzer):
        """大運吉凶判定（凶運）のテスト"""
        # 不利な大運の例
        result = analyzer.analyze_daeun_fortune(
            day_stem="甲",
            day_branch="寅",
            hour_stem="己",
            hour_branch="申",
            month_branch="子",  # 冬生まれ
            daeun_stem="己",  # 甲→己 = 大凶（甲己合）
            daeun_branch="申",  # 寅→申 = 大凶（寅申沖）
        )
        assert result in ["凶", "大凶"]

    def test_daeun_fortune_neutral(self, analyzer):
        """大運吉凶判定（平運）のテスト"""
        # 中立的な大運の例
        result = analyzer.analyze_daeun_fortune(
            day_stem="甲",
            day_branch="辰",
            hour_stem="戊",
            hour_branch="辰",
            month_branch="辰",  # 春生まれ
            daeun_stem="戊",  # 甲→戊 = 吉
            daeun_branch="辰",  # 辰→辰 = 平
        )
        assert result in ["平", "吉"]

    def test_fortune_to_score_conversion(self, analyzer):
        """吉凶→スコア変換のテスト"""
        assert analyzer._fortune_to_score("大吉") == 2.0
        assert analyzer._fortune_to_score("吉") == 1.0
        assert analyzer._fortune_to_score("平") == 0.0
        assert analyzer._fortune_to_score("凶") == -1.0
        assert analyzer._fortune_to_score("大凶") == -2.0

    def test_score_to_fortune_conversion(self, analyzer):
        """スコア→吉凶変換のテスト"""
        assert analyzer._score_to_fortune(2.0) == "大吉"
        assert analyzer._score_to_fortune(1.0) == "吉"
        assert analyzer._score_to_fortune(0.0) == "平"
        assert analyzer._score_to_fortune(-1.0) == "凶"
        assert analyzer._score_to_fortune(-2.0) == "大凶"

    def test_comprehensive_daeun_analysis(self, analyzer):
        """総合的な大運分析テスト（実例）"""
        # 1986年5月26日生まれ（辛未日）の例
        result = analyzer.analyze_daeun_fortune(
            day_stem="辛",
            day_branch="未",
            hour_stem="辛",
            hour_branch="卯",
            month_branch="巳",  # 夏生まれ
            daeun_stem="癸",  # 辛→癸 = 吉
            daeun_branch="酉",  # 9月運（秋）
        )
        # 辛金は秋が吉なので、全体的に吉運
        assert result in ["吉", "大吉", "平"]


class TestRealWorldScenarios:
    """実際のシナリオテスト"""

    @pytest.fixture
    def analyzer(self):
        """テスト用のFortuneAnalyzerインスタンス"""
        return FortuneAnalyzer()

    def test_scenario_test_taro(self, analyzer):
        """テスト太郎（1990年1月15日14:30）のテスト"""
        # 実際の命式に基づくテストケース
        # TODO: 実際の命式データで検証
        pass

    def test_scenario_test_hanako(self, analyzer):
        """テスト花子（1995年6月20日10:15）のテスト"""
        # 実際の命式に基づくテストケース
        # TODO: 実際の命式データで検証
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
