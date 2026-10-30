"""
Rule execution engine for RuleRoute.
Evaluates deterministic propositional rules for language recommendations and project catalog retrieval.
"""

from typing import List, Dict, Any, Optional
from .catalog import PROJECT_CATALOG
from .validation import validate_user_profile
from .diagnostics import DecisionTrace


def evaluate_language_rules(
    profile: Dict[str, Any],
    trace: Optional[DecisionTrace] = None
) -> List[Dict[str, str]]:
    """
    Deterministic rule-based engine mapping user preferences to suitable programming languages.
    Preserves exact logic and text from the original notebook while emitting detailed decision trace events.

    Args:
        profile: Validated user profile dictionary.
        trace: Optional DecisionTrace accumulator for diagnostics.

    Returns:
        List of language recommendations with rationale.
    """
    domain = profile['preferred_domain']
    level = profile['experience_level']
    interest = profile['main_interest'].lower()
    languages: List[Dict[str, str]] = []

    if trace is not None:
        trace.record(
            stage='Domain Routing',
            action=f"Evaluate domain classification rule for '{domain}'",
            result=f"Active rule branch: {domain} engine rules",
            status='info'
        )

    if domain == 'AI/ML':
        languages.append({
            'language': 'Python',
            'rationale': 'De facto standard for AI/ML with industry-dominant ecosystems (PyTorch, TensorFlow, scikit-learn).',
            'triggered_rule': 'AI/ML baseline rule (Always applicable for domain)',
        })
        if trace is not None:
            trace.record(
                stage='Language Evaluation',
                action='AI/ML baseline ecosystem check',
                result='Python selected as foundation language for AI/ML workflows',
                status='success'
            )

        if level in ['Intermediate', 'Advanced']:
            languages.append({
                'language': 'C++',
                'rationale': 'Critical for high-performance model deployment, embedded edge AI, and tensor engine inference.',
                'triggered_rule': 'AI/ML advanced performance rule (Intermediate or Advanced level)',
            })
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action=f"Evaluate performance requirement rule (level='{level}' in ['Intermediate', 'Advanced'])",
                    result='C++ selected for systems-level model compilation and high-throughput tensor operations',
                    status='success'
                )
        else:
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action=f"Evaluate performance requirement rule (level='{level}' in ['Intermediate', 'Advanced'])",
                    result='C++ omitted (target experience level is Beginner; focused on high-level Python APIs)',
                    status='info'
                )

    elif domain == 'Web Development':
        front_condition = 'front' in interest or 'full' in interest or level == 'Beginner'
        if front_condition:
            languages.append({
                'language': 'JavaScript / TypeScript',
                'rationale': 'Universal browser language powering modern reactive interfaces (React, Vue) and full-stack frameworks.',
                'triggered_rule': "Web UI / Full-stack rule ('front' in interest, 'full' in interest, or Beginner level)",
            })
            if trace is not None:
                matched_reason = "interest contains 'front' or 'full'" if ('front' in interest or 'full' in interest) else "level is Beginner"
                trace.record(
                    stage='Language Evaluation',
                    action="Check client/full-stack condition ('front' in interest or 'full' in interest or Beginner level)",
                    result=f"JavaScript / TypeScript selected ({matched_reason})",
                    status='success'
                )
        else:
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action="Check client/full-stack condition ('front' in interest or 'full' in interest or Beginner level)",
                    result="JavaScript / TypeScript condition not met",
                    status='info'
                )

        back_condition = 'back' in interest or 'api' in interest or 'full' in interest
        if back_condition:
            languages.append({
                'language': 'Python',
                'rationale': 'Fast, expressive backend frameworks (FastAPI, Django) ideal for microservice and API architecture.',
                'triggered_rule': "Web Backend rule ('back', 'api', or 'full' in interest)",
            })
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action="Check backend condition ('back', 'api', or 'full' in interest)",
                    result="Python selected for backend service and API development",
                    status='success'
                )

            if level == 'Advanced':
                languages.append({
                    'language': 'Go (Golang)',
                    'rationale': 'Superb concurrency models and high-throughput networking for scalable distributed systems.',
                    'triggered_rule': 'High-concurrency backend rule (Advanced level + Backend interest)',
                })
                if trace is not None:
                    trace.record(
                        stage='Language Evaluation',
                        action="Check distributed concurrency rule (level == 'Advanced')",
                        result="Go (Golang) selected for high-throughput distributed microservices",
                        status='success'
                    )
            else:
                if trace is not None:
                    trace.record(
                        stage='Language Evaluation',
                        action="Check distributed concurrency rule (level == 'Advanced')",
                        result=f"Go omitted (experience level '{level}' is below Advanced threshold)",
                        status='info'
                    )
        else:
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action="Check backend condition ('back', 'api', or 'full' in interest)",
                    result="Backend condition not triggered by interest keywords",
                    status='info'
                )

    elif domain == 'App Development':
        if 'android' in interest:
            languages.append({
                'language': 'Kotlin',
                'rationale': "Google's official preferred modern language for robust native Android mobile development.",
                'triggered_rule': "Native Android rule ('android' in interest)",
            })
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action="Check Android native rule ('android' in interest)",
                    result="Kotlin selected for official native Android development",
                    status='success'
                )
        elif 'cross' in interest or level == 'Beginner':
            languages.append({
                'language': 'Dart (Flutter)',
                'rationale': 'Single codebase compiling to performant native iOS and Android applications smoothly.',
                'triggered_rule': "Cross-platform / Accessible mobile rule ('cross' in interest or Beginner level)",
            })
            if trace is not None:
                matched_reason = "interest contains 'cross'" if 'cross' in interest else "level is Beginner"
                trace.record(
                    stage='Language Evaluation',
                    action="Check cross-platform mobile condition ('cross' in interest or Beginner level)",
                    result=f"Dart (Flutter) selected ({matched_reason})",
                    status='success'
                )
        else:
            languages.append({
                'language': 'Kotlin',
                'rationale': 'Modern native mobile architecture standard with coroutine-based asynchronous processing.',
                'triggered_rule': 'General mobile engineering standard rule (Intermediate / Advanced fallback)',
            })
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action="Evaluate mobile architecture default rule (Intermediate/Advanced non-cross)",
                    result="Kotlin selected for modern native mobile engineering",
                    status='success'
                )

    elif domain == 'Data Science':
        languages.append({
            'language': 'Python',
            'rationale': 'Unrivaled data manipulation and analytical ecosystem (Pandas, NumPy, Matplotlib, Scipy).',
            'triggered_rule': 'Data Science baseline rule (Always applicable for domain)',
        })
        if trace is not None:
            trace.record(
                stage='Language Evaluation',
                action='Data science baseline analysis check',
                result='Python selected for exploratory analysis, numerical computing, and visualization',
                status='success'
            )

        if level in ['Intermediate', 'Advanced']:
            languages.append({
                'language': 'SQL',
                'rationale': 'Foundational language for relational database querying, data aggregation, and ETL workflows.',
                'triggered_rule': 'Data querying rule (Intermediate or Advanced level)',
            })
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action=f"Check database analysis rule (level='{level}' in ['Intermediate', 'Advanced'])",
                    result='SQL selected for relational warehousing, ETL, and structured dataset aggregation',
                    status='success'
                )
        else:
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action=f"Check database analysis rule (level='{level}' in ['Intermediate', 'Advanced'])",
                    result='SQL omitted (curriculum for Beginner prioritizes core Python syntax)',
                    status='info'
                )

    elif domain == 'Automation':
        languages.append({
            'language': 'Python',
            'rationale': 'Premier scripting language with versatile libraries for web scraping (BeautifulSoup) and OS automation.',
            'triggered_rule': 'Automation baseline rule (Always applicable for domain)',
        })
        if trace is not None:
            trace.record(
                stage='Language Evaluation',
                action='Automation scripting check',
                result='Python selected for web scraping, file orchestration, and OS automation',
                status='success'
            )

        if level in ['Intermediate', 'Advanced']:
            languages.append({
                'language': 'Bash / Shell',
                'rationale': 'Essential for UNIX/Linux server orchestration, job scheduling, and continuous deployment workflows.',
                'triggered_rule': 'System orchestration rule (Intermediate or Advanced level)',
            })
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action=f"Check OS orchestration rule (level='{level}' in ['Intermediate', 'Advanced'])",
                    result='Bash / Shell selected for Linux daemon management and CI/CD automation',
                    status='success'
                )
        else:
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action=f"Check OS orchestration rule (level='{level}' in ['Intermediate', 'Advanced'])",
                    result='Bash / Shell omitted (Beginner automation focused on Python scripting)',
                    status='info'
                )

    elif domain == 'Game Development':
        unity_condition = 'unity' in interest or level in ['Beginner', 'Intermediate']
        if unity_condition:
            languages.append({
                'language': 'C#',
                'rationale': 'Primary scripting language for Unity Engine, combining approachable syntax with high performance.',
                'triggered_rule': "Unity game engine rule ('unity' in interest or Beginner/Intermediate level)",
            })
            if trace is not None:
                matched_reason = "interest mentions 'unity'" if 'unity' in interest else f"experience level is {level}"
                trace.record(
                    stage='Language Evaluation',
                    action="Check rapid game prototyping condition ('unity' in interest or Beginner/Intermediate level)",
                    result=f"C# selected for Unity Engine gameplay programming ({matched_reason})",
                    status='success'
                )
        else:
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action="Check rapid game prototyping condition ('unity' in interest or Beginner/Intermediate level)",
                    result="C# condition not triggered",
                    status='info'
                )

        engine_condition = 'engine' in interest or level == 'Advanced'
        if engine_condition:
            languages.append({
                'language': 'C++',
                'rationale': 'Standard systems language for Unreal Engine and custom high-performance 3D graphics engines.',
                'triggered_rule': "Low-level engine rule ('engine' in interest or Advanced level)",
            })
            if trace is not None:
                matched_reason = "interest mentions 'engine'" if 'engine' in interest else "experience level is Advanced"
                trace.record(
                    stage='Language Evaluation',
                    action="Check low-level engine architecture condition ('engine' in interest or Advanced level)",
                    result=f"C++ selected for Unreal Engine and low-level rendering pipelines ({matched_reason})",
                    status='success'
                )
        else:
            if trace is not None:
                trace.record(
                    stage='Language Evaluation',
                    action="Check low-level engine architecture condition ('engine' in interest or Advanced level)",
                    result="C++ condition not triggered",
                    status='info'
                )

    if not languages and trace is not None:
        trace.record(
            stage='Language Evaluation',
            action='Aggregate language recommendations',
            result='No language rules triggered by the provided keyword combinations.',
            status='warning'
        )

    return languages


def evaluate_project_rules(
    profile: Dict[str, Any],
    trace: Optional[DecisionTrace] = None
) -> List[Dict[str, str]]:
    """
    Rule catalog matching providing achievable, tailored undergraduate projects.
    Filters the 18 canonical project ideas by domain and difficulty, falling back to domain if no match.

    Args:
        profile: Validated user profile dictionary.
        trace: Optional DecisionTrace accumulator for diagnostics.

    Returns:
        List of matching project dictionaries.
    """
    domain = profile['preferred_domain']
    difficulty = profile['preferred_difficulty']

    matched = [p for p in PROJECT_CATALOG if p['domain'] == domain and p['difficulty'] == difficulty]

    if matched:
        if trace is not None:
            project_names = ", ".join(f"'{p['name']}'" for p in matched)
            trace.record(
                stage='Project Matching',
                action=f"Filter catalog for domain='{domain}' and difficulty='{difficulty}'",
                result=f"Exact match found ({len(matched)} project): {project_names}",
                status='success'
            )
    else:
        # Fallback matching from original notebook logic
        matched = [p for p in PROJECT_CATALOG if p['domain'] == domain]
        if trace is not None:
            trace.record(
                stage='Project Matching',
                action=f"Filter catalog for domain='{domain}' and difficulty='{difficulty}' (no exact match)",
                result=f"Fallback invoked: retrieved {len(matched)} general projects for domain '{domain}'",
                status='warning'
            )

    return matched


def recommend(
    profile: Any,
    return_trace: bool = True
) -> Dict[str, Any]:
    """
    Orchestrates validation, language rules, and project matching.
    Preserves exact output schema from the original notebook while appending structured trace metadata.

    Args:
        profile: User profile dictionary to evaluate.
        return_trace: Whether to include decision trace in the output dictionary.

    Returns:
        Dictionary containing status, message, languages, projects, and execution trace.
    """
    trace = DecisionTrace() if return_trace else None

    is_valid, validation_msg = validate_user_profile(profile)
    if not is_valid:
        if trace is not None:
            trace.record(
                stage='Profile Validation',
                action='Check required fields, data types, and supported boundaries',
                result=f"Validation failed: {validation_msg}",
                status='error'
            )
        return {
            'status': 'Error',
            'message': validation_msg,
            'languages': [],
            'projects': [],
            'trace': trace.to_list() if trace is not None else [],
            'profile': profile if isinstance(profile, dict) else {},
        }

    if trace is not None:
        trace.record(
            stage='Profile Validation',
            action='Check required fields, data types, and supported boundaries',
            result='Validation successful: Profile adheres to all schema constraints',
            status='success'
        )

    languages = evaluate_language_rules(profile, trace=trace)
    projects = evaluate_project_rules(profile, trace=trace)

    if trace is not None:
        trace.record(
            stage='Recommendation Synthesis',
            action='Synthesize language recommendations and matching project ideas',
            result=f"Recommendations complete: {len(languages)} language(s), {len(projects)} project(s)",
            status='success'
        )

    return {
        'status': 'Success',
        'message': 'Recommendations computed successfully.',
        'languages': languages,
        'projects': projects,
        'trace': trace.to_list() if trace is not None else [],
        'profile': profile,
    }
