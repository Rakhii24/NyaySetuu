import os
from datetime import datetime, timedelta
from app.models.user import User
from app.models.case import Case, LawImpact
from app.models.law import Law
from app.models.notification import Notification

def seed_demo_environment():
    """Seeds in-memory demo data if the database is currently empty."""
    if User.objects.count() > 0:
        return

    print("🌱 Initializing NyaySetu In-Memory Demo Dataset...")

    # 1. Seed Demo Users
    users_data = [
        {
            "username": "judge",
            "email": "judge@nyaysetu.gov.in",
            "password": "password123",
            "role": "judge",
            "full_name": "Hon. Justice R. K. Sharma",
            "phone": "+91-9876543210"
        },
        {
            "username": "lawyer",
            "email": "lawyer@nyaysetu.gov.in",
            "password": "password123",
            "role": "lawyer",
            "full_name": "Advocate Priya Verma",
            "phone": "+91-9876543211"
        },
        {
            "username": "citizen",
            "email": "citizen@nyaysetu.gov.in",
            "password": "password123",
            "role": "citizen",
            "full_name": "Rahul Sharma",
            "phone": "+91-9876543212"
        },
        {
            "username": "RAKHI",
            "email": "rakhi@nyaysetu.gov.in",
            "password": "rakhi123",
            "role": "lawyer",
            "full_name": "Advocate Rakhi Desai",
            "phone": "+91-9876543213"
        }
    ]

    created_users = {}
    for u_data in users_data:
        pwd = u_data.pop("password")
        user = User(**u_data)
        user.set_password(pwd)
        user.save()
        created_users[user.role] = user

    print(f"✅ Created {len(users_data)} judicial user accounts.")

    # 2. Seed Statutory Laws
    laws_data = [
        {
            "title": "Criminal Procedure (Bail Reform) Amendment Act 2024",
            "description": "Statutory amendment mandating Section 41A compliance, personal liberty safeguards, and regulated pre-trial custody.",
            "full_text": """AN ACT further to amend the Code of Criminal Procedure.
Section 41A is hereby amended to mandate immediate notice before arrest in all non-heinous offenses.
Provided that where the accused complies with the notice, no arrest shall be made unless recorded in writing with special judicial sanction.
This amendment aims to reduce unnecessary pretrial custody and align strictly with Article 21 fundamental rights.""",
            "lawyer_summary": "Mandatory Section 41A compliance. Notice is now a strict prerequisite for arrest in non-heinous crimes, shifting the burden of proof to the state to justify custodial detention.",
            "citizen_summary": "The law now requires police to serve a formal 'Section 41A notice' before any arrest in non-violent cases, protecting citizens from unlawful or arbitrary detention.",
            "category": "Criminal",
            "sections": ["Section 41A", "Article 21", "Section 436A"],
            "effective_date": datetime.utcnow() - timedelta(days=60),
            "scraped_source": "Gazette of India (Extraordinary, Part II)",
            "impact_reasoning": "Direct impact on active bail petitions and undertrial detentions exceeding 90 days."
        },
        {
            "title": "Digital Personal Data Protection (DPDP) Act 2023",
            "description": "Comprehensive regulatory framework for digital data processing, consent architecture, and privacy enforcement.",
            "full_text": """AN ACT to provide for the processing of digital personal data in a manner that recognises both the right of individuals to protect their personal data and the need to process such personal data for lawful purposes.
Sections 6, 7 and 9 prescribe strict algorithmic audits and fiduciary obligations for commercial platforms.""",
            "lawyer_summary": "Imposes statutory penalties up to 250 Crores INR for non-consensual data profiling. Requires compliance audits and affects pending IP and cyber intermediary disputes.",
            "citizen_summary": "Empowers citizens with ownership over personal data. Apps and websites cannot store or share personal details without explicit, revocable consent.",
            "category": "Technology",
            "sections": ["Section 6", "Section 7", "Section 9", "Section 28"],
            "effective_date": datetime.utcnow() - timedelta(days=180),
            "scraped_source": "Ministry of Law & Justice Bulletin",
            "impact_reasoning": "Significant bearing on pending privacy writ petitions and corporate intellectual property suits."
        },
        {
            "title": "Bharatiya Nyaya Sanhita (BNS) Transition Guidelines 2024",
            "description": "Procedural alignment replacing IPC provisions, standardizing community service sentencing and electronic summons.",
            "full_text": """Guidelines issued by the Ministry of Home Affairs and Supreme Court for harmonious transition from Indian Penal Code to Bharatiya Nyaya Sanhita.
Introduces alternative sentencing mechanisms including community service for minor infractions and mandatory video recording of search procedures.""",
            "lawyer_summary": "Statutory transition matrix between IPC sections and BNS equivalents. Authorizes digital FIRs and audio-video electronic evidentiary submissions under Section 61.",
            "citizen_summary": "Modernizes court processes by allowing electronic notices and community service instead of jail time for small first-time offenses.",
            "category": "Criminal",
            "sections": ["Section 4", "Section 61", "Section 103"],
            "effective_date": datetime.utcnow() - timedelta(days=90),
            "scraped_source": "Supreme Court e-Committee Gazette",
            "impact_reasoning": "Applicable across all criminal trial dockets and ongoing charge-sheet validations."
        },
        {
            "title": "Industrial Relations & Worker Welfare Code Amendment 2024",
            "description": "Statutory revisions regarding fixed-term employment contracts, severance norms, and tribunal dispute resolution timeframes.",
            "full_text": """AN ACT to consolidate and amend the laws relating to Trade Unions, conditions of employment in industrial establishment or undertaking, investigation and settlement of industrial disputes.
Mandates maximum 45-day conciliation periods for union grievances and universal health coverage contributions.""",
            "lawyer_summary": "Accelerates labour appellate timelines, enforces bipartite arbitration, and establishes mandatory social security deposits for industrial lay-offs.",
            "citizen_summary": "Ensures workers receive faster resolution of unpaid wages and illegal dismissals within fixed 45-day tribunal schedules.",
            "category": "Labour",
            "sections": ["Section 22", "Section 35", "Section 58"],
            "effective_date": datetime.utcnow() - timedelta(days=120),
            "scraped_source": "Ministry of Labour Gazette",
            "impact_reasoning": "Directly influences ongoing labour union appeals and workplace compensation claims."
        }
    ]

    saved_laws = []
    for l_data in laws_data:
        law = Law(**l_data)
        law.save()
        saved_laws.append(law)

    print(f"✅ Created {len(saved_laws)} statutory enactments.")

    # 3. Seed Realistic Cases
    now = datetime.utcnow()
    cases_data = [
        {
            "case_number": "CRA/450/2022",
            "title": "State of Maharashtra vs. Rajesh Kumar",
            "description": "Criminal appeal regarding protest participation. Accused detained for 14 months without charge confirmation. Violation of Section 41A procedural standards.",
            "case_type": "Criminal",
            "court_type": "High Court",
            "court_name": "Bombay High Court",
            "high_court_name": "Bombay High Court",
            "urgency": "High",
            "number_of_evidence": 12,
            "hearing_count": 8,
            "stage": "Appeal",
            "social_sensitivity": 8,
            "filing_date": now - timedelta(days=580),
            "status": "Processed",
            "predicted_priority": "High",
            "priority_score": 0.94,
            "priority_reasoning": "Prolonged undertrial detention (14+ months) in non-heinous classification coupled with procedural non-compliance under Section 41A elevates case to critical judicial priority.",
            "lawyer": created_users.get("lawyer"),
            "citizen": created_users.get("citizen"),
            "impact_reports": [
                LawImpact(
                    precedent_title=saved_laws[0].title,
                    precedent_citation="CrPC (Bail Reform) §41A",
                    source="Statutory Enactment",
                    relevance_score=0.96,
                    impact_level="High",
                    url="https://nyaysetu.gov.in/laws/bail-reform-2024",
                    impact_explanation="Directly qualifies for immediate bail relief under amended Section 41A due to lack of written justification for continued detention.",
                    section_matches=["Section 41A", "Article 21"],
                    raw_score=0.96
                )
            ]
        },
        {
            "case_number": "BA/99/2024",
            "title": "Mohd. Tariq vs. State NCT of Delhi",
            "description": "Urgent regular bail application. Investigating authority failed to provide pre-arrest notice. Invoking amended statutory provisions.",
            "case_type": "Criminal",
            "court_type": "Session Court",
            "court_name": "Patiala House Court",
            "high_court_name": "Delhi High Court",
            "urgency": "High",
            "number_of_evidence": 4,
            "hearing_count": 3,
            "stage": "Pre-trial",
            "social_sensitivity": 7,
            "filing_date": now - timedelta(days=22),
            "status": "Processed",
            "predicted_priority": "High",
            "priority_score": 0.91,
            "priority_reasoning": "Fresh bail petition involving non-compliance of Section 41A statutory directives. Requires expedited judicial examination to safeguard Article 21 rights.",
            "lawyer": created_users.get("lawyer"),
            "citizen": created_users.get("citizen"),
            "impact_reports": [
                LawImpact(
                    precedent_title=saved_laws[0].title,
                    precedent_citation="CrPC §41A Amendment",
                    source="Statutory Enactment",
                    relevance_score=0.93,
                    impact_level="High",
                    url="https://nyaysetu.gov.in/laws/bail-reform-2024",
                    impact_explanation="Mandatory pre-arrest notice was bypassed by prosecution; grounds for immediate bail consideration established.",
                    section_matches=["Section 41A"],
                    raw_score=0.93
                )
            ]
        },
        {
            "case_number": "CS/1029/2023",
            "title": "Apex Infotech Ltd. vs. Swift Data Systems",
            "description": "Intellectual property infringement suit with cross-allegations of consumer telemetry data scraping without consent.",
            "case_type": "Civil",
            "court_type": "High Court",
            "court_name": "Delhi High Court",
            "high_court_name": "Delhi High Court",
            "urgency": "Medium",
            "number_of_evidence": 48,
            "hearing_count": 5,
            "stage": "Trial",
            "social_sensitivity": 5,
            "filing_date": now - timedelta(days=240),
            "status": "Processed",
            "predicted_priority": "Medium",
            "priority_score": 0.68,
            "priority_reasoning": "Commercial dispute involving multi-party evidence examination and proprietary telemetry algorithms. Balanced pendency factor.",
            "lawyer": created_users.get("lawyer"),
            "citizen": created_users.get("citizen"),
            "impact_reports": [
                LawImpact(
                    precedent_title=saved_laws[1].title,
                    precedent_citation="DPDP Act 2023 §6",
                    source="Statutory Enactment",
                    relevance_score=0.88,
                    impact_level="High",
                    url="https://nyaysetu.gov.in/laws/dpdp-2023",
                    impact_explanation="Alleged unconsented telemetry data scraping falls squarely under Section 6 fiduciary liabilities, altering evidence admissibility.",
                    section_matches=["Section 6", "Section 9"],
                    raw_score=0.88
                )
            ]
        },
        {
            "case_number": "LCA/55/2021",
            "title": "Textile Workers Federation vs. Premier Mills Corp",
            "description": "Labour appellate dispute regarding mass plant closure and retrenchment compensation for 620 factory operatives.",
            "case_type": "Labour",
            "court_type": "High Court",
            "court_name": "Karnataka High Court",
            "high_court_name": "Karnataka High Court",
            "urgency": "High",
            "number_of_evidence": 134,
            "hearing_count": 18,
            "stage": "Appeal",
            "social_sensitivity": 9,
            "filing_date": now - timedelta(days=920),
            "status": "Processed",
            "predicted_priority": "High",
            "priority_score": 0.89,
            "priority_reasoning": "Severe social impact touching 600+ families coupled with high pendency (2.5+ years) triggers emergency appellate review.",
            "lawyer": created_users.get("lawyer"),
            "citizen": created_users.get("citizen"),
            "impact_reports": [
                LawImpact(
                    precedent_title=saved_laws[3].title,
                    precedent_citation="Worker Welfare Code §35",
                    source="Statutory Enactment",
                    relevance_score=0.85,
                    impact_level="High",
                    url="https://nyaysetu.gov.in/laws/labour-code-2024",
                    impact_explanation="Applies strict 45-day statutory conciliation window and mandates escrow deposits for pending worker retrenchment payouts.",
                    section_matches=["Section 35", "Section 58"],
                    raw_score=0.85
                )
            ]
        },
        {
            "case_number": "PIL/12/2024",
            "title": "Citizens for Clean Air vs. Union of India",
            "description": "Public Interest Litigation seeking statutory compliance on vehicular emission monitoring across urban transit corridors.",
            "case_type": "Civil",
            "court_type": "Supreme Court",
            "court_name": "Supreme Court of India",
            "high_court_name": "Supreme Court",
            "urgency": "Medium",
            "number_of_evidence": 85,
            "hearing_count": 6,
            "stage": "Trial",
            "social_sensitivity": 10,
            "filing_date": now - timedelta(days=110),
            "status": "Processed",
            "predicted_priority": "High",
            "priority_score": 0.86,
            "priority_reasoning": "Pan-jurisdictional environmental implications with high social sensitivity rating (10/10) warrants accelerated hearings.",
            "lawyer": created_users.get("lawyer"),
            "citizen": created_users.get("citizen"),
            "impact_reports": []
        },
        {
            "case_number": "CC/781/2023",
            "title": "Ramesh Chandra vs. National Insurance Co.",
            "description": "Consumer protection petition regarding repudiation of critical illness health insurance claims.",
            "case_type": "Civil",
            "court_type": "District Court",
            "court_name": "Gautam Buddha Nagar District Forum",
            "high_court_name": "Allahabad High Court",
            "urgency": "Medium",
            "number_of_evidence": 16,
            "hearing_count": 4,
            "stage": "Trial",
            "social_sensitivity": 4,
            "filing_date": now - timedelta(days=310),
            "status": "Processed",
            "predicted_priority": "Medium",
            "priority_score": 0.58,
            "priority_reasoning": "Standard consumer dispute docket with documented evidence records and standard trial stage progression.",
            "lawyer": created_users.get("lawyer"),
            "citizen": created_users.get("citizen"),
            "impact_reports": []
        },
        {
            "case_number": "SCC/334/2024",
            "title": "Sunil Sharma vs. Metro Property Developers",
            "description": "Summary recovery suit for delayed commercial possession with interest claim.",
            "case_type": "Civil",
            "court_type": "Session Court",
            "court_name": "Saket District Court",
            "high_court_name": "Delhi High Court",
            "urgency": "Low",
            "number_of_evidence": 9,
            "hearing_count": 2,
            "stage": "Pre-trial",
            "social_sensitivity": 2,
            "filing_date": now - timedelta(days=80),
            "status": "Processed",
            "predicted_priority": "Low",
            "priority_score": 0.35,
            "priority_reasoning": "Commercial claim within initial discovery phase with low societal sensitivity and recent filing date.",
            "lawyer": created_users.get("lawyer"),
            "citizen": created_users.get("citizen"),
            "impact_reports": []
        },
        {
            "case_number": "BNS/41/2024",
            "title": "State of Gujarat vs. Vikram Patel & Ors.",
            "description": "Criminal indictment under transition provisions of BNS Section 61 involving electronic surveillance logs.",
            "case_type": "Criminal",
            "court_type": "Session Court",
            "court_name": "Ahmedabad City Civil & Sessions Court",
            "high_court_name": "Gujarat High Court",
            "urgency": "High",
            "number_of_evidence": 32,
            "hearing_count": 5,
            "stage": "Trial",
            "social_sensitivity": 6,
            "filing_date": now - timedelta(days=65),
            "status": "Processed",
            "predicted_priority": "High",
            "priority_score": 0.84,
            "priority_reasoning": "First-instance interpretation of electronic evidence admissibility requirements under Section 61 of the new penal code.",
            "lawyer": created_users.get("lawyer"),
            "citizen": created_users.get("citizen"),
            "impact_reports": [
                LawImpact(
                    precedent_title=saved_laws[2].title,
                    precedent_citation="BNS Guidelines §61",
                    source="Statutory Enactment",
                    relevance_score=0.91,
                    impact_level="High",
                    url="https://nyaysetu.gov.in/laws/bns-guidelines-2024",
                    impact_explanation="Mandatory videography requirements under BNS guidelines apply directly to the contested physical seizure evidence.",
                    section_matches=["Section 61", "Section 103"],
                    raw_score=0.91
                )
            ]
        }
    ]

    saved_cases = []
    for c_data in cases_data:
        case = Case(**c_data)
        case.save()
        saved_cases.append(case)

    # Link affecting cases to laws
    saved_laws[0].affecting_cases = [str(saved_cases[0].id), str(saved_cases[1].id)]
    saved_laws[0].affected_count = 2
    saved_laws[0].save()

    saved_laws[1].affecting_cases = [str(saved_cases[2].id)]
    saved_laws[1].affected_count = 1
    saved_laws[1].save()

    saved_laws[2].affecting_cases = [str(saved_cases[7].id)]
    saved_laws[2].affected_count = 1
    saved_laws[2].save()

    saved_laws[3].affecting_cases = [str(saved_cases[3].id)]
    saved_laws[3].affected_count = 1
    saved_laws[3].save()

    print(f"✅ Created {len(saved_cases)} court cases across judicial tiers.")

    # 4. Seed User Notifications
    for role_name, user_obj in created_users.items():
        Notification(
            user=user_obj,
            title="Judicial AI Initialized",
            message="Welcome to NyaySetu. Prioritization model and statutory impact engine are synchronized.",
            type="System",
            read=False,
            link_to_id=str(saved_laws[0].id)
        ).save()
        Notification(
            user=user_obj,
            title="High Impact Statutory Alert",
            message=f"New statutory amendment '{saved_laws[0].title}' impacts 2 pending cases on your docket.",
            type="LawImpact",
            read=False,
            link_to_id=str(saved_laws[0].id)
        ).save()

    print("✅ Seeded system notifications.")
    print("🎉 NyaySetu In-Memory Environment is ready.")
