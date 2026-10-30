"""
Comprehensive unit tests for the RuleRoute recommendation engine.
Validates input validation, categorical boundaries, rule evaluations,
catalog coverage, decision tracing, and fallback logic.
"""

import pytest
from recommendation_engine.catalog import (
    SUPPORTED_DOMAINS,
    SUPPORTED_LEVELS,
    SUPPORTED_DIFFICULTIES,
    PROJECT_CATALOG,
    DEMO_PROFILES,
)
from recommendation_engine.validation import validate_user_profile
from recommendation_engine.rules import (
    evaluate_language_rules,
    evaluate_project_rules,
    recommend,
)
from recommendation_engine.diagnostics import DecisionTrace


# ---------------------------------------------------------------------------
# 1. Validation Tests
# ---------------------------------------------------------------------------

def test_validate_valid_profile():
    profile = {
        'experience_level': 'Beginner',
        'preferred_domain': 'AI/ML',
        'main_interest': 'Neural networks and reflex agents',
        'preferred_difficulty': 'Easy',
    }
    is_valid, msg = validate_user_profile(profile)
    assert is_valid is True
    assert "valid" in msg.lower()


def test_validate_non_dict_input():
    for bad_input in [None, "invalid_string", [1, 2, 3], 42]:
        is_valid, msg = validate_user_profile(bad_input)
        assert is_valid is False
        assert "expected a dictionary" in msg.lower()


def test_validate_missing_keys():
    required_keys = ['experience_level', 'preferred_domain', 'main_interest', 'preferred_difficulty']
    base_profile = {
        'experience_level': 'Beginner',
        'preferred_domain': 'AI/ML',
        'main_interest': 'Python scripting',
        'preferred_difficulty': 'Easy',
    }
    for key in required_keys:
        incomplete = {k: v for k, v in base_profile.items() if k != key}
        is_valid, msg = validate_user_profile(incomplete)
        assert is_valid is False
        assert f"Missing required profile field: '{key}'" in msg


def test_validate_unsupported_domain():
    profile = {
        'experience_level': 'Beginner',
        'preferred_domain': 'Quantum Computing',
        'main_interest': 'Qubits',
        'preferred_difficulty': 'Easy',
    }
    is_valid, msg = validate_user_profile(profile)
    assert is_valid is False
    assert "Unsupported domain" in msg
    assert "Quantum Computing" in msg


def test_validate_unsupported_experience_level():
    profile = {
        'experience_level': 'Master',
        'preferred_domain': 'AI/ML',
        'main_interest': 'Deep learning',
        'preferred_difficulty': 'Easy',
    }
    is_valid, msg = validate_user_profile(profile)
    assert is_valid is False
    assert "Unsupported experience level" in msg
    assert "Master" in msg


def test_validate_unsupported_difficulty():
    profile = {
        'experience_level': 'Beginner',
        'preferred_domain': 'AI/ML',
        'main_interest': 'Deep learning',
        'preferred_difficulty': 'Super-Hard',
    }
    is_valid, msg = validate_user_profile(profile)
    assert is_valid is False
    assert "Unsupported difficulty" in msg
    assert "Super-Hard" in msg


def test_validate_empty_and_whitespace_interest():
    for empty_val in ["", "   ", "\t\n  "]:
        profile = {
            'experience_level': 'Beginner',
            'preferred_domain': 'AI/ML',
            'main_interest': empty_val,
            'preferred_difficulty': 'Easy',
        }
        is_valid, msg = validate_user_profile(profile)
        assert is_valid is False
        assert "cannot be empty or whitespace only" in msg.lower()


def test_validate_invalid_interest_type():
    for bad_interest in [123, ["Python"], {"topic": "AI"}, None]:
        profile = {
            'experience_level': 'Beginner',
            'preferred_domain': 'AI/ML',
            'main_interest': bad_interest,
            'preferred_difficulty': 'Easy',
        }
        is_valid, msg = validate_user_profile(profile)
        assert is_valid is False
        assert "Invalid main interest type" in msg


# ---------------------------------------------------------------------------
# 2. Domain & Experience Level Rules Coverage
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("domain", SUPPORTED_DOMAINS)
def test_all_supported_domains_evaluate(domain):
    profile = {
        'experience_level': 'Beginner',
        'preferred_domain': domain,
        'main_interest': 'General exploration',
        'preferred_difficulty': 'Easy',
    }
    result = recommend(profile)
    assert result['status'] == 'Success'
    assert len(result['languages']) > 0
    assert len(result['projects']) > 0


@pytest.mark.parametrize("level", SUPPORTED_LEVELS)
def test_all_supported_levels_evaluate(level):
    profile = {
        'experience_level': level,
        'preferred_domain': 'Data Science',
        'main_interest': 'Statistical modeling',
        'preferred_difficulty': 'Medium',
    }
    result = recommend(profile)
    assert result['status'] == 'Success'
    assert any(lang['language'] == 'Python' for lang in result['languages'])
    if level in ['Intermediate', 'Advanced']:
        assert any(lang['language'] == 'SQL' for lang in result['languages'])
    else:
        assert not any(lang['language'] == 'SQL' for lang in result['languages'])


@pytest.mark.parametrize("difficulty", SUPPORTED_DIFFICULTIES)
def test_all_supported_difficulties_evaluate(difficulty):
    profile = {
        'experience_level': 'Intermediate',
        'preferred_domain': 'Automation',
        'main_interest': 'Shell scripting and bots',
        'preferred_difficulty': difficulty,
    }
    result = recommend(profile)
    assert result['status'] == 'Success'
    assert len(result['projects']) == 1
    assert result['projects'][0]['difficulty'] == difficulty


# ---------------------------------------------------------------------------
# 3. Specific Keyword Matching Tests
# ---------------------------------------------------------------------------

def test_web_development_keyword_rules():
    # Frontend condition: contains 'front' -> JavaScript / TypeScript
    p_front = {
        'experience_level': 'Intermediate',
        'preferred_domain': 'Web Development',
        'main_interest': 'Modern frontend components with Vue',
        'preferred_difficulty': 'Easy',
    }
    res_front = recommend(p_front)
    languages = [l['language'] for l in res_front['languages']]
    assert 'JavaScript / TypeScript' in languages
    assert 'Python' not in languages

    # Backend condition: contains 'api' -> Python
    p_back = {
        'experience_level': 'Intermediate',
        'preferred_domain': 'Web Development',
        'main_interest': 'RESTful API microservices',
        'preferred_difficulty': 'Medium',
    }
    res_back = recommend(p_back)
    languages = [l['language'] for l in res_back['languages']]
    assert 'Python' in languages
    assert 'Go (Golang)' not in languages

    # Fullstack + Advanced: contains 'full' and level='Advanced' -> JS/TS, Python, and Go
    p_full_adv = {
        'experience_level': 'Advanced',
        'preferred_domain': 'Web Development',
        'main_interest': 'Full-stack distributed applications',
        'preferred_difficulty': 'Hard',
    }
    res_full_adv = recommend(p_full_adv)
    languages = [l['language'] for l in res_full_adv['languages']]
    assert 'JavaScript / TypeScript' in languages
    assert 'Python' in languages
    assert 'Go (Golang)' in languages


def test_app_development_keyword_rules():
    # 'android' -> Kotlin
    p_android = {
        'experience_level': 'Intermediate',
        'preferred_domain': 'App Development',
        'main_interest': 'Native Android app with Jetpack Compose',
        'preferred_difficulty': 'Medium',
    }
    res = recommend(p_android)
    languages = [l['language'] for l in res['languages']]
    assert 'Kotlin' in languages
    assert 'Dart (Flutter)' not in languages

    # 'cross' -> Dart (Flutter)
    p_cross = {
        'experience_level': 'Intermediate',
        'preferred_domain': 'App Development',
        'main_interest': 'Cross-platform mobile apps for iOS and desktop',
        'preferred_difficulty': 'Medium',
    }
    res_cross = recommend(p_cross)
    languages = [l['language'] for l in res_cross['languages']]
    assert 'Dart (Flutter)' in languages

    # Beginner without keywords -> Dart (Flutter)
    p_beg = {
        'experience_level': 'Beginner',
        'preferred_domain': 'App Development',
        'main_interest': 'Mobile user interfaces',
        'preferred_difficulty': 'Easy',
    }
    res_beg = recommend(p_beg)
    languages = [l['language'] for l in res_beg['languages']]
    assert 'Dart (Flutter)' in languages


def test_game_development_keyword_rules():
    # 'unity' -> C#
    p_unity = {
        'experience_level': 'Advanced',
        'preferred_domain': 'Game Development',
        'main_interest': 'Unity Shader Graph and gameplay scripting',
        'preferred_difficulty': 'Medium',
    }
    res = recommend(p_unity)
    languages = [l['language'] for l in res['languages']]
    assert 'C#' in languages

    # 'engine' -> C++
    p_engine = {
        'experience_level': 'Beginner',
        'preferred_domain': 'Game Development',
        'main_interest': 'Vulkan engine rendering loops',
        'preferred_difficulty': 'Hard',
    }
    res_engine = recommend(p_engine)
    languages = [l['language'] for l in res_engine['languages']]
    assert 'C++' in languages
    # For Beginner, C# is also matched because level in ['Beginner', 'Intermediate']
    assert 'C#' in languages


# ---------------------------------------------------------------------------
# 4. Canonical 18 Projects Catalog Coverage
# ---------------------------------------------------------------------------

def test_catalog_size_and_attributes():
    assert len(PROJECT_CATALOG) == 18, "Catalog must retain all 18 canonical project ideas"
    for proj in PROJECT_CATALOG:
        assert 'domain' in proj
        assert 'difficulty' in proj
        assert 'name' in proj
        assert 'language' in proj
        assert 'description' in proj
        assert 'reason' in proj
        assert proj['domain'] in SUPPORTED_DOMAINS
        assert proj['difficulty'] in SUPPORTED_DIFFICULTIES


def test_all_18_projects_retrievable():
    # Each domain x difficulty pair must match exactly one project in the catalog
    for domain in SUPPORTED_DOMAINS:
        for difficulty in SUPPORTED_DIFFICULTIES:
            profile = {
                'experience_level': 'Beginner',
                'preferred_domain': domain,
                'main_interest': 'Testing catalog match',
                'preferred_difficulty': difficulty,
            }
            matched = evaluate_project_rules(profile)
            assert len(matched) == 1
            assert matched[0]['domain'] == domain
            assert matched[0]['difficulty'] == difficulty


# ---------------------------------------------------------------------------
# 5. Original Notebook Assertions Preservation
# ---------------------------------------------------------------------------

def test_original_notebook_demonstrations():
    # 1. Beginner in AI/ML
    p1 = DEMO_PROFILES[0]['profile']
    res1 = recommend(p1)
    assert res1['status'] == 'Success', "Profile 1 recommendation failed"
    assert res1['languages'][0]['language'] == 'Python'
    assert res1['projects'][0]['name'] == 'Smart Vacuum Cleaner Simulation & Reflex Agent'

    # 2. Intermediate Web Developer
    p2 = DEMO_PROFILES[1]['profile']
    res2 = recommend(p2)
    assert res2['status'] == 'Success', "Profile 2 recommendation failed"
    p2_langs = [l['language'] for l in res2['languages']]
    assert 'JavaScript / TypeScript' in p2_langs
    assert 'Python' in p2_langs
    assert res2['projects'][0]['name'] == 'Collaborative Note-Sharing & Discussion Platform'

    # 3. Advanced Game Developer
    p3 = DEMO_PROFILES[2]['profile']
    res3 = recommend(p3)
    assert res3['status'] == 'Success', "Profile 3 recommendation failed"
    assert res3['languages'][0]['language'] == 'C++'
    assert res3['projects'][0]['name'] == 'Custom OpenGL/Vulkan 3D Rendering Engine'

    # 4. Beginner in Automation
    p4 = DEMO_PROFILES[3]['profile']
    res4 = recommend(p4)
    assert res4['status'] == 'Success', "Profile 4 recommendation failed"
    assert res4['languages'][0]['language'] == 'Python'
    assert res4['projects'][0]['name'] == 'Automated E-Commerce Price Monitor & Notification Bot'

    # 5. Invalid Profile Edge Case
    p_inv = DEMO_PROFILES[4]['profile']
    res_inv = recommend(p_inv)
    assert res_inv['status'] == 'Error', "Invalid profile was not caught by validator"
    assert "Unsupported domain 'Quantum Computing'" in res_inv['message']

    # Cross-profile assertions from original notebook
    assert res1['languages'] != res2['languages'], "Distinct profiles must yield distinct languages"
    assert res1['projects'] != res2['projects'], "Distinct profiles must yield distinct projects"


# ---------------------------------------------------------------------------
# 6. Decision Trace & Diagnostics Tests
# ---------------------------------------------------------------------------

def test_decision_trace_generation():
    profile = {
        'experience_level': 'Intermediate',
        'preferred_domain': 'AI/ML',
        'main_interest': 'Computer Vision',
        'preferred_difficulty': 'Medium',
    }
    result = recommend(profile, return_trace=True)
    assert 'trace' in result
    trace = result['trace']
    assert len(trace) >= 4  # Validation, Domain Routing, Language Eval, Project Matching, Synthesis

    stages = [step['stage'] for step in trace]
    assert 'Profile Validation' in stages
    assert 'Domain Routing' in stages
    assert 'Language Evaluation' in stages
    assert 'Project Matching' in stages


def test_decision_trace_on_validation_failure():
    profile = {
        'experience_level': 'Beginner',
        'preferred_domain': 'Blockchain',
        'main_interest': 'Smart contracts',
        'preferred_difficulty': 'Easy',
    }
    result = recommend(profile, return_trace=True)
    assert result['status'] == 'Error'
    assert len(result['trace']) > 0
    assert result['trace'][0]['status'] == 'error'


# ---------------------------------------------------------------------------
# 7. Fallback Matching Logic
# ---------------------------------------------------------------------------

def test_project_matching_fallback_behavior():
    # If difficulty does not match any entry, fallback returns all projects for domain
    profile_nonexistent_diff = {
        'preferred_domain': 'AI/ML',
        'preferred_difficulty': 'NonExistentDifficulty',
    }
    matched = evaluate_project_rules(profile_nonexistent_diff)
    assert len(matched) == 3
    assert all(p['domain'] == 'AI/ML' for p in matched)

