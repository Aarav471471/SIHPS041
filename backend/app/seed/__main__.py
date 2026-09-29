import argparse
import sys
import os
import random
from datetime import datetime, timedelta
import uuid

# Add the parent directory to sys.path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db import SessionLocal, engine
from app.models.all import (
    Base, Organization, Site, User, Module, Attempt, AttemptAnswer, 
    AttemptStep, Certificate, SectorEnum, RoleEnum, LanguageEnum, CertStatusEnum
)
from app.security import get_password_hash

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    if db.query(Organization).count() > 0:
        print("Database already seeded.")
        db.close()
        return

    print("Seeding database...")
    
    # 1. Organization
    org = Organization(name="Government of Jharkhand")
    db.add(org)
    db.commit()
    
    # 2. Sites
    sites = [
        Site(org_id=org.id, code="DHN-01", name="BCCL Dhanbad", sector=SectorEnum.coal, district="Dhanbad"),
        Site(org_id=org.id, code="BOK-01", name="BSL Bokaro", sector=SectorEnum.steel, district="Bokaro"),
        Site(org_id=org.id, code="KOD-01", name="Koderma Mica Unit", sector=SectorEnum.mica, district="Koderma"),
    ]
    db.add_all(sites)
    db.commit()

    # 3. Users: Admin & Supervisors
    admin = User(
        name="System Admin", 
        phone="admin@suraksha.demo", 
        pin_hash=get_password_hash("Admin@123"), 
        role=RoleEnum.admin,
        worker_code="A-000001"
    )
    sup1 = User(
        name="Supervisor Ramesh", 
        phone="9999999991", 
        pin_hash=get_password_hash("1234"), 
        role=RoleEnum.supervisor, 
        site_id=sites[0].id,
        worker_code="S-000001"
    )
    sup2 = User(
        name="Supervisor Sita", 
        phone="9999999992", 
        pin_hash=get_password_hash("1234"), 
        role=RoleEnum.supervisor, 
        site_id=sites[1].id,
        worker_code="S-000002"
    )
    db.add_all([admin, sup1, sup2])
    
    # Demo worker
    demo_worker = User(
        name="Demo Worker", 
        phone="9000000001", 
        pin_hash=get_password_hash("1234"), 
        role=RoleEnum.worker, 
        site_id=sites[0].id,
        language=LanguageEnum.sat,
        worker_code="W-000001"
    )
    db.add(demo_worker)
    db.commit()

    # 4. Modules
    modules = [
        Module(code="fire", title_key="mod_fire_title", pass_mark=70),
        Module(code="gas", title_key="mod_gas_title", pass_mark=70),
        Module(code="machinery", title_key="mod_mach_title", is_lite=True, pass_mark=70),
        Module(code="electrical", title_key="mod_elec_title", is_lite=True, pass_mark=70),
        Module(code="ppe", title_key="mod_ppe_title", is_lite=True, pass_mark=70),
    ]
    db.add_all(modules)
    db.commit()

    # Generate 80 fictional workers
    print("Generating workers and attempts...")
    workers = []
    for i in range(80):
        w = User(
            name=f"Worker {i+2}", 
            phone=f"800000{i:04d}", 
            pin_hash=get_password_hash("1234"), 
            role=RoleEnum.worker, 
            site_id=random.choice(sites).id,
            language=random.choice(list(LanguageEnum)),
            worker_code=f"W-{uuid.uuid4().hex[:6].upper()}"
        )
        workers.append(w)
    db.add_all(workers)
    db.commit()

    # Generate attempts and certificates
    for w in workers:
        # 0 to 3 attempts per worker
        for _ in range(random.randint(0, 3)):
            mod = random.choice(modules)
            passed = random.choice([True, True, False])
            score = random.randint(70, 100) if passed else random.randint(30, 69)
            
            attempt_id = str(uuid.uuid4())
            sub_time = datetime.utcnow() - timedelta(days=random.randint(1, 30))
            att = Attempt(
                id=attempt_id,
                user_id=w.id,
                module_code=mod.code,
                started_at=sub_time - timedelta(minutes=10),
                submitted_at=sub_time,
                client_score=score,
                server_score=score,
                ar_score=score,
                assess_score=score,
                passed=passed
            )
            db.add(att)
            db.flush()

            if passed:
                cert_status = CertStatusEnum.valid
                revoked_reason = None
                revoked_at = None
                
                # Make a few revoked
                if random.random() < 0.05:
                    cert_status = CertStatusEnum.revoked
                    revoked_reason = "Violation of safety protocol"
                    revoked_at = sub_time + timedelta(days=1)
                
                # Make a few expired by setting issued_at a year ago
                issued = sub_time
                expires = issued + timedelta(days=mod.validity_days)
                if random.random() < 0.1:
                    issued = datetime.utcnow() - timedelta(days=400)
                    expires = issued + timedelta(days=mod.validity_days)

                cert = Certificate(
                    id=str(uuid.uuid4()),
                    user_id=w.id,
                    module_code=mod.code,
                    attempt_id=att.id,
                    score=score,
                    issued_at=issued,
                    expires_at=expires,
                    status=cert_status,
                    payload_json="{}",
                    signature_b64="dummy_sig",
                    revoked_reason=revoked_reason,
                    revoked_at=revoked_at
                )
                db.add(cert)
    
    db.commit()
    print("Seed complete.")
    
    # Check ES256 key
    from app.services.crypto_service import ensure_keys
    ensure_keys()
    db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--if-empty", action="store_true")
    args = parser.parse_args()
    seed_db()
