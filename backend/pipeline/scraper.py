"""
LegalX AI Knowledge Centre - Legal Content Scraper
Fetches raw legal text from public government/legal sources.
"""

import httpx
from bs4 import BeautifulSoup
import asyncio
import logging

logger = logging.getLogger(__name__)

LEGAL_SOURCES = {
    "pocso": {
        "name": "POCSO Act",
        "full_name": "Protection of Children from Sexual Offences Act, 2012",
        "urls": [
            "https://wcd.nic.in/sites/default/files/POCSO%20Act%2C%202012.pdf",
        ],
        "fallback_text": """
        The Protection of Children from Sexual Offences Act (POCSO), 2012 is a comprehensive law in India 
        to protect children from offences of sexual assault, sexual harassment and pornography, 
        while safeguarding the interests of the child at every stage of the judicial process.
        
        The Act defines a child as any person below eighteen years of age, and regards the best 
        interests and well-being of the child as being of paramount importance at every stage.
        
        Key Provisions:
        - Section 3-10: Defines sexual assault, aggravated sexual assault, and their punishments
        - Section 11-12: Defines sexual harassment of a child
        - Section 13-15: Covers use of child for pornographic purposes
        - Section 19: Mandatory reporting - any person aware of an offence must report it
        - Section 21: Failure to report is an offence punishable with imprisonment
        - Section 28: Special Court for trial of offences under the Act
        - Section 35: Time limit for completion of trial (one year)
        - Section 42: Act to have overriding effect
        
        Punishments:
        - Penetrative sexual assault: Minimum 7 years, extendable to life imprisonment
        - Aggravated penetrative sexual assault: Minimum 10 years, extendable to life or death penalty
        - Sexual harassment: Up to 3 years imprisonment and fine
        - Child pornography: Up to 5 years imprisonment and fine for first conviction
        
        Key Features:
        - Child-friendly procedures for recording evidence
        - Special courts for speedy trial
        - Burden of proof on the accused
        - Medical examination of the child within 24 hours
        - Confidentiality of child's identity
        - Compensation to child victims
        
        Who benefits: All children below 18 years, both boys and girls, regardless of gender.
        The Act recognizes that both males and females can be victims of sexual offences.
        """,
    },
    "consumer_protection": {
        "name": "Consumer Protection Act",
        "full_name": "Consumer Protection Act, 2019",
        "urls": [],
        "fallback_text": """
        The Consumer Protection Act, 2019 is a landmark legislation in India that replaced the 
        Consumer Protection Act of 1986. It provides for better protection of the interests of 
        consumers and establishes authorities for timely and effective administration and settlement 
        of consumer disputes.
        
        Definition of Consumer: A person who buys any goods or avails any services for consideration, 
        does not include a person who buys goods for resale or commercial purposes.
        
        Key Rights of Consumers (Section 2(9)):
        1. Right to Safety - protection against hazardous goods
        2. Right to Information - about quality, quantity, price of goods/services
        3. Right to Choose - access to variety of goods at competitive prices
        4. Right to be Heard - interests will receive due consideration
        5. Right to Seek Redressal - against unfair trade practices
        6. Right to Consumer Education - right to acquire knowledge
        
        Key Authorities:
        - Central Consumer Protection Authority (CCPA) - established under Section 10
        - National Consumer Disputes Redressal Commission (NCDRC) - above Rs 2 crore
        - State Consumer Disputes Redressal Commission (SCDRC) - Rs 1-2 crore
        - District Consumer Disputes Redressal Commission (DCDRC) - up to Rs 1 crore
        
        New Features in 2019 Act:
        - E-commerce regulations included
        - Product liability provisions (Chapter VI)
        - Unfair contracts addressed
        - Mediation as dispute resolution mechanism
        - Penalties for misleading advertisements
        
        Penalties:
        - Misleading advertisements: up to Rs 10 lakh (first offence), Rs 50 lakh (subsequent)
        - Spurious/adulterated goods causing grievous hurt: up to 7 years imprisonment
        - Spurious goods causing death: up to life imprisonment
        - Unfair trade practices: fines ranging from Rs 25,000 to Rs 5 lakh
        
        E-commerce provisions: Platforms must disclose seller details, country of origin, 
        grievance redressal mechanism, and cannot indulge in unfair trade practices.
        """,
    },
    "cyber_crime": {
        "name": "Cyber Crime Laws",
        "full_name": "Information Technology Act, 2000 & Cyber Crime Laws",
        "urls": [],
        "fallback_text": """
        Cyber Crime Laws in India are primarily governed by the Information Technology Act, 2000 
        (amended in 2008) along with provisions of the Indian Penal Code (IPC) and the newly 
        enacted Bharatiya Nyaya Sanhita (BNS) 2023.
        
        The IT Act 2000 defines various cyber offences and prescribes punishments for the same.
        
        Major Cyber Crimes and Punishments:
        
        Section 43 - Damage to Computer Systems:
        - Unauthorized access, downloading data, introducing viruses
        - Penalty: Compensation up to Rs 1 crore to affected party
        
        Section 66 - Computer Related Offences:
        - Dishonestly or fraudulently doing acts under Section 43
        - Punishment: Up to 3 years imprisonment or fine up to Rs 5 lakh or both
        
        Section 66A (Struck down) - Offensive Messages (struck down by Supreme Court in 2015)
        
        Section 66B - Dishonestly receiving stolen computer resource:
        - Punishment: Up to 3 years imprisonment or fine up to Rs 1 lakh
        
        Section 66C - Identity Theft:
        - Fraudulently using another's electronic signature, password
        - Punishment: Up to 3 years imprisonment and fine up to Rs 1 lakh
        
        Section 66D - Cheating by Personation using Computer Resource:
        - Punishment: Up to 3 years imprisonment and fine up to Rs 1 lakh
        
        Section 66E - Violation of Privacy:
        - Publishing private images without consent
        - Punishment: Up to 3 years imprisonment or fine up to Rs 2 lakh
        
        Section 66F - Cyber Terrorism:
        - Threatening unity, integrity, sovereignty of India
        - Punishment: Life imprisonment
        
        Section 67 - Publishing Obscene Material in Electronic Form:
        - Punishment: First conviction - 3 years and fine Rs 5 lakh; subsequent - 5 years
        
        Section 72 - Breach of Confidentiality and Privacy:
        - Unauthorized disclosure of information
        - Punishment: Up to 2 years imprisonment or fine up to Rs 1 lakh
        
        Common Cyber Crimes:
        - Phishing: Fraudulent emails/websites to steal information
        - Online Banking Fraud: Unauthorized access to bank accounts
        - Cyber Stalking: Online harassment and following
        - Ransomware: Malware that encrypts data and demands ransom
        - Social Media Fraud: Fake profiles, morphed images
        
        Reporting Cyber Crime:
        - National Cyber Crime Reporting Portal: cybercrime.gov.in
        - Helpline: 1930
        - Local police cyber cell
        
        Who can benefit: Any individual, organization, or government body that is a victim 
        of cyber crimes can seek redressal under these laws.
        """,
    },
    "rti": {
        "name": "Right to Information (RTI) Act",
        "full_name": "Right to Information Act, 2005",
        "urls": [],
        "fallback_text": """
        The Right to Information Act, 2005 (RTI Act) is a powerful law that empowers citizens 
        to seek information from public authorities. It promotes transparency and accountability 
        in the working of every public authority.
        
        Key Definitions:
        - Information: Any material in any form including records, documents, memos, emails, 
          opinions, advices, press releases, circulars, orders, logbooks, contracts, reports, 
          papers, samples, models, data material held in any electronic form
        - Public Authority: Any authority or body established under the Constitution, or by any 
          law made by Parliament or State Legislature
        - Public Information Officer (PIO): Officer designated to provide information
        
        Who Can File RTI:
        - Any citizen of India can file an RTI application
        - Organizations and companies cannot file RTI (only individuals)
        - No reason needs to be given for seeking information
        
        How to File RTI:
        1. Write application to the Public Information Officer (PIO) of concerned department
        2. Pay fee of Rs 10 (central government), varies by state
        3. Application can be in English, Hindi or official language of the area
        4. Can be filed online at rtionline.gov.in
        
        Time Limits:
        - PIO must respond within 30 days of receipt
        - If information concerns life or liberty: within 48 hours
        - If request sent to wrong PIO, transfer within 5 days, total response in 30 days
        
        Exemptions (Section 8):
        - Information affecting sovereignty, integrity, security of India
        - Information expressly forbidden by court
        - Cabinet papers, Council of Ministers deliberations
        - Personal information not related to public activity
        - Information given in fiduciary capacity
        
        Appeal Process:
        - First Appeal: To appellate authority within 30 days, decision in 30-45 days
        - Second Appeal: To Central/State Information Commission within 90 days
        
        Penalties (Section 20):
        - If PIO fails to give information without reasonable cause: Rs 250 per day, maximum Rs 25,000
        - Persistent refusal: Disciplinary action
        - Giving false information: Same penalty as above
        
        Information Commission:
        - Central Information Commission (CIC) for central government
        - State Information Commissions (SIC) for state governments
        - Commissioners have same powers as civil court
        
        Key RTI Achievements in India:
        - Exposed corruption in public works
        - Revealed misuse of government funds
        - Helped obtain documents for legal cases
        - Improved accountability of public servants
        """,
    },
    "gst": {
        "name": "GST Registration",
        "full_name": "Goods and Services Tax (GST) Registration & Law",
        "urls": [],
        "fallback_text": """
        Goods and Services Tax (GST) is India's most significant indirect tax reform, implemented 
        on July 1, 2017. It replaced a complex system of central and state taxes with a unified, 
        destination-based, multi-stage tax.
        
        GST Structure:
        - CGST: Central Goods and Services Tax (collected by Central Government)
        - SGST: State Goods and Services Tax (collected by State Government)
        - IGST: Integrated Goods and Services Tax (inter-state supplies, collected by Centre)
        - UTGST: Union Territory Goods and Services Tax
        
        GST Registration Requirements:
        
        Mandatory Registration:
        - Annual aggregate turnover exceeds Rs 40 lakhs (goods) or Rs 20 lakhs (services)
        - In special category states: Rs 20 lakhs (goods), Rs 10 lakhs (services)
        - Businesses making inter-state supply of goods
        - E-commerce operators and sellers on e-commerce platforms
        - Input Service Distributors (ISD)
        - Non-Resident Taxable Persons
        - Persons who are required to pay tax under reverse charge mechanism
        - Agents of a supplier
        
        Voluntary Registration:
        - Businesses below threshold can register voluntarily to avail Input Tax Credit (ITC)
        
        Documents Required for GST Registration:
        1. PAN card of business owner/entity
        2. Aadhaar card of authorized signatory
        3. Proof of business registration (Certificate of Incorporation, Partnership deed, etc.)
        4. Identity and address proof of promoters/partners
        5. Address proof of principal place of business
        6. Bank account details
        7. Digital Signature (for companies)
        
        GST Registration Process:
        1. Visit GST Portal (gst.gov.in)
        2. Click on 'Register Now' under Services tab
        3. Select New Registration
        4. Fill Part A: Enter PAN, Mobile, Email - get TRN (Temporary Reference Number)
        5. Fill Part B: Business details, promoters, authorized signatory, places of business
        6. Upload documents
        7. Verification: Via DSC, e-Sign, or EVC
        8. ARN generated; GSTIN issued within 3-7 working days
        
        GST Tax Slabs:
        - 0%: Essential items (foodgrains, milk, eggs, vegetables)
        - 5%: Household necessities (cooking oil, sugar, spices, tea, coffee)
        - 12%: Computers, processed food, business class tickets
        - 18%: Most goods and services, hair oil, soaps, toothpaste
        - 28%: Luxury items, sin goods (tobacco, aerated drinks, automobiles)
        
        Input Tax Credit (ITC):
        - Businesses can claim credit for GST paid on inputs
        - Reduces cascading effect of taxes
        - Must file monthly returns to claim ITC
        
        GST Returns:
        - GSTR-1: Monthly return for outward supplies (by 11th of next month)
        - GSTR-3B: Monthly summary return (by 20th of next month)
        - GSTR-9: Annual return
        
        Penalties for Non-Compliance:
        - Late filing: Rs 100 per day (CGST) + Rs 100 per day (SGST) = Rs 200/day
        - Maximum penalty: Rs 5,000
        - Tax evasion: 100% of tax amount as penalty
        - Serious evasion (above Rs 5 crore): Imprisonment up to 5 years
        
        Benefits of GST:
        - Elimination of cascading taxes
        - Unified national market
        - Improved compliance through technology
        - Composition scheme for small businesses (1-6% tax, simplified compliance)
        """,
    },
}


async def scrape_legal_content(topic_key: str) -> str:
    """
    Fetch legal content for a given topic.
    Tries online sources first, falls back to curated legal text.
    """
    topic = LEGAL_SOURCES.get(topic_key)
    if not topic:
        raise ValueError(f"Unknown topic: {topic_key}")

    # Try to scrape from URLs
    for url in topic.get("urls", []):
        try:
            async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
                resp = await client.get(url)
                if resp.status_code == 200 and "text/html" in resp.headers.get("content-type", ""):
                    soup = BeautifulSoup(resp.text, "lxml")
                    # Remove script/style tags
                    for tag in soup(["script", "style", "nav", "footer", "header"]):
                        tag.decompose()
                    text = soup.get_text(separator="\n", strip=True)
                    if len(text) > 500:
                        logger.info(f"Scraped {len(text)} chars from {url}")
                        return text
        except Exception as e:
            logger.warning(f"Failed to scrape {url}: {e}")

    # Use curated fallback legal text (still processed through AI pipeline)
    logger.info(f"Using curated legal text for {topic_key}")
    return topic["fallback_text"].strip()


def get_all_topics() -> list[dict]:
    """Return metadata for all legal topics."""
    return [
        {"key": key, "name": topic["name"], "full_name": topic["full_name"]}
        for key, topic in LEGAL_SOURCES.items()
    ]


def get_topic_metadata(topic_key: str) -> dict:
    """Return metadata for a single topic."""
    topic = LEGAL_SOURCES.get(topic_key)
    if not topic:
        return {}
    return {
        "key": topic_key,
        "name": topic["name"],
        "full_name": topic["full_name"],
    }
