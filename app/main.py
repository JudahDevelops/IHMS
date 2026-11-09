import sys
import os

# 🚨 Ensure 'app' package can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path
import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import get_db, engine, DATABASE_URL
from app.model import User, Role
from app.route import api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print(f"🔗 [DEBUG] Trying to connect to database: {DATABASE_URL}")

def run_migrations() -> None:
    project_root = Path(__file__).resolve().parent.parent
    alembic_ini_path = project_root / "alembic.ini"
    alembic_dir = project_root / "alembic"
    versions_dir = alembic_dir / "versions"

    print(f"🔍 [DEBUG] Looking for alembic.ini at: {alembic_ini_path}")

    if not alembic_ini_path.exists():
        raise FileNotFoundError(f"❌ [DEBUG] Alembic config not found at {alembic_ini_path}")

    # 1. Ensure directories exist
    alembic_dir.mkdir(parents=True, exist_ok=True)
    versions_dir.mkdir(parents=True, exist_ok=True)

    # 2. Ensure script.py.mako exists
    mako_path = alembic_dir / "script.py.mako"
    if not mako_path.exists():
        print("📝 [DEBUG] Creating missing script.py.mako template...")
        mako_content = '''"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
'''
        mako_path.write_text(mako_content, encoding="utf-8")

    # 3. Ensure env.py exists
    env_path = alembic_dir / "env.py"
    if not env_path.exists():
        print("📝 [DEBUG] Creating missing env.py template...")
        env_content = '''import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
load_dotenv()

from app.database import Base
from app.model import User, Role, user_role_association

config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''
        env_path.write_text(env_content, encoding="utf-8")

    # 4. Configure Alembic with absolute path
    alembic_cfg = Config(str(alembic_ini_path))
    alembic_cfg.config_ini_section = "alembic"  # Force the section name
    alembic_cfg.set_main_option("script_location", str(alembic_dir))

    print(f"📂 [DEBUG] Checking for migrations in: {versions_dir}")

    if not any(versions_dir.iterdir()):
        print("📝 [DEBUG] No migrations found. Auto-generating initial migration...")
        command.revision(alembic_cfg, autogenerate=True, message="Initial auto-generated migration")
        print("✅ [DEBUG] Migration file generated.")

    print("⚙️ [DEBUG] Applying database migrations...")
    command.upgrade(alembic_cfg, "head")
    print("✅ [DEBUG] Database migrations applied successfully.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🌟 [DEBUG] FastAPI starting up...")
    try:
        await asyncio.to_thread(run_migrations)
    except Exception as e:
        print(f"❌ [DEBUG] Migration FAILED: {e}")
        raise
    yield
    print("🛑 [DEBUG] FastAPI shutting down...")

app = FastAPI(
    title="Intelligent Hostel Management System (IHMS) API",
    description="Full CRUD, real-time search, and optimized pagination API for all IHMS models.",
    version="1.0.0",
    lifespan=lifespan
)

# Register all model routes with /api/v1 and root prefixes
app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router)

@app.get("/")
def read_root():
    return {
        "message": "Intelligent Hostel Management System (IHMS) API is running!",
        "system": "IHMS - Automated Complaint Triage and Escalation",
        "institution": "Nile University of Nigeria",
        "documentation": "/docs"
    }

@app.post("/seed-data")
def seed_data(db: Session = Depends(get_db)):
    from app.model import (
        User, Role, MaintenanceUnit, TriageKeyword,
        ComplaintCategoryEnum, ComplaintUrgencyEnum
    )
    
    # 1. Seed Core Roles
    role_names = ["student", "maintenance_officer", "hall_warden", "administrator"]
    created_roles = {}
    for r_name in role_names:
        role = db.query(Role).filter_by(name=r_name).first()
        if not role:
            role = Role(name=r_name, description=f"IHMS {r_name.replace('_', ' ').title()} Role")
            db.add(role)
        created_roles[r_name] = role
    db.flush()

    # 2. Seed Maintenance Units
    units_data = [
        ("PLUMBING", "Plumbing Maintenance Unit", "plumbing@nileuniversity.edu.ng"),
        ("ELECTRICAL", "Electrical Maintenance Unit", "electrical@nileuniversity.edu.ng"),
        ("CARPENTRY", "Carpentry & Joinery Unit", "carpentry@nileuniversity.edu.ng"),
        ("SANITATION", "Sanitation & Cleaning Unit", "sanitation@nileuniversity.edu.ng"),
        ("GENERAL", "General / Civil Works Unit", "maintenance@nileuniversity.edu.ng"),
    ]
    for code, name, email in units_data:
        unit = db.query(MaintenanceUnit).filter_by(code=code).first()
        if not unit:
            unit = MaintenanceUnit(code=code, name=name, email=email, description=f"{name} dispatch queue")
            db.add(unit)
    db.flush()

    # 3. Seed Default Triage Keywords from Research Paper Table IV
    keywords_data = [
        ("burst", ComplaintCategoryEnum.PLUMBING, ComplaintUrgencyEnum.URGENT),
        ("flood", ComplaintCategoryEnum.PLUMBING, ComplaintUrgencyEnum.URGENT),
        ("no water", ComplaintCategoryEnum.PLUMBING, ComplaintUrgencyEnum.URGENT),
        ("spark", ComplaintCategoryEnum.ELECTRICAL, ComplaintUrgencyEnum.URGENT),
        ("exposed wire", ComplaintCategoryEnum.ELECTRICAL, ComplaintUrgencyEnum.URGENT),
        ("broken lock", ComplaintCategoryEnum.CARPENTRY, ComplaintUrgencyEnum.URGENT),
        ("leaking tap", ComplaintCategoryEnum.PLUMBING, ComplaintUrgencyEnum.NORMAL),
        ("blocked drain", ComplaintCategoryEnum.PLUMBING, ComplaintUrgencyEnum.NORMAL),
        ("faulty socket", ComplaintCategoryEnum.ELECTRICAL, ComplaintUrgencyEnum.NORMAL),
        ("broken bed", ComplaintCategoryEnum.CARPENTRY, ComplaintUrgencyEnum.NORMAL),
        ("paint", ComplaintCategoryEnum.OTHER, ComplaintUrgencyEnum.LOW),
        ("loose handle", ComplaintCategoryEnum.CARPENTRY, ComplaintUrgencyEnum.LOW),
        ("squeaking door", ComplaintCategoryEnum.CARPENTRY, ComplaintUrgencyEnum.LOW),
    ]
    for kw, cat, urg in keywords_data:
        kw_record = db.query(TriageKeyword).filter_by(keyword=kw, category=cat).first()
        if not kw_record:
            kw_record = TriageKeyword(keyword=kw, category=cat, urgency=urg, weight=1)
            db.add(kw_record)
    db.flush()

    # 4. Seed Test Administrator User
    test_user = db.query(User).filter_by(username="admin").first()
    if not test_user:
        test_user = User(
            username="admin",
            email="admin@nileuniversity.edu.ng",
            password="hashed_admin_password",
            first_name="IHMS",
            last_name="Administrator"
        )
        test_user.roles.append(created_roles["administrator"])
        db.add(test_user)

    db.commit()
    return {
        "message": "IHMS foundational data seeded successfully!",
        "seeded_roles": list(created_roles.keys()),
        "seeded_units": [u[0] for u in units_data],
        "keywords_count": len(keywords_data)
    }

if __name__ == "__main__":
    print("🌐 [DEBUG] Starting Uvicorn server...")
    # Run from app folder or root, it doesn't matter now
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)