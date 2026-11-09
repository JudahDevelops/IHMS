"""Create IHMS complete normalized schema

Revision ID: c1f8e9a2b3d4
Revises: 89a416482db9
Create Date: 2026-11-02 15:10:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c1f8e9a2b3d4'
down_revision: Union[str, None] = '89a416482db9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Update existing 'roles' table
    op.add_column('roles', sa.Column('description', sa.String(length=255), nullable=True))
    op.add_column('roles', sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))

    # 2. Update existing 'users' table
    op.add_column('users', sa.Column('first_name', sa.String(length=50), server_default='', nullable=False))
    op.add_column('users', sa.Column('last_name', sa.String(length=50), server_default='', nullable=False))
    op.add_column('users', sa.Column('phone_number', sa.String(length=20), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))

    # 3. Update existing 'user_role' table
    op.add_column('user_role', sa.Column('assigned_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))

    # 4. Create 'maintenance_units' table
    op.create_table(
        'maintenance_units',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=30), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_maintenance_units_id'), 'maintenance_units', ['id'], unique=False)
    op.create_index(op.f('ix_maintenance_units_code'), 'maintenance_units', ['code'], unique=True)

    # 5. Create 'hostels' table
    op.create_table(
        'hostels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('gender_target', sa.String(length=20), server_default='mixed', nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('total_capacity', sa.Integer(), server_default='0', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hostels_id'), 'hostels', ['id'], unique=False)
    op.create_index(op.f('ix_hostels_name'), 'hostels', ['name'], unique=True)
    op.create_index(op.f('ix_hostels_code'), 'hostels', ['code'], unique=True)

    # 6. Create 'rooms' table
    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hostel_id', sa.Integer(), nullable=False),
        sa.Column('room_number', sa.String(length=20), nullable=False),
        sa.Column('floor', sa.Integer(), server_default='1', nullable=False),
        sa.Column('capacity', sa.Integer(), server_default='4', nullable=False),
        sa.Column('current_occupancy', sa.Integer(), server_default='0', nullable=False),
        sa.Column('is_available', sa.Boolean(), server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['hostel_id'], ['hostels.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('hostel_id', 'room_number', name='uq_hostel_room_number')
    )
    op.create_index(op.f('ix_rooms_id'), 'rooms', ['id'], unique=False)
    op.create_index(op.f('ix_rooms_hostel_id'), 'rooms', ['hostel_id'], unique=False)

    # 7. Create 'bed_spaces' table
    op.create_table(
        'bed_spaces',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('bed_label', sa.String(length=10), nullable=False),
        sa.Column('is_occupied', sa.Boolean(), server_default='0', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('room_id', 'bed_label', name='uq_room_bed_label')
    )
    op.create_index(op.f('ix_bed_spaces_id'), 'bed_spaces', ['id'], unique=False)
    op.create_index(op.f('ix_bed_spaces_room_id'), 'bed_spaces', ['room_id'], unique=False)

    # 8. Create 'student_profiles' table
    op.create_table(
        'student_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('matric_number', sa.String(length=50), nullable=False),
        sa.Column('gender', sa.String(length=20), nullable=False),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('department', sa.String(length=100), nullable=False),
        sa.Column('faculty', sa.String(length=100), nullable=True),
        sa.Column('fee_cleared', sa.Boolean(), server_default='0', nullable=False),
        sa.Column('fee_cleared_at', sa.DateTime(), nullable=True),
        sa.Column('emergency_contact_name', sa.String(length=100), nullable=True),
        sa.Column('emergency_contact_phone', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_student_profiles_id'), 'student_profiles', ['id'], unique=False)
    op.create_index(op.f('ix_student_profiles_matric_number'), 'student_profiles', ['matric_number'], unique=True)
    op.create_index(op.f('ix_student_profiles_user_id'), 'student_profiles', ['user_id'], unique=True)

    # 9. Create 'staff_profiles' table
    op.create_table(
        'staff_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('staff_number', sa.String(length=50), nullable=False),
        sa.Column('unit_id', sa.Integer(), nullable=True),
        sa.Column('assigned_hostel_id', sa.Integer(), nullable=True),
        sa.Column('designation', sa.String(length=100), nullable=True),
        sa.Column('office_location', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['assigned_hostel_id'], ['hostels.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['unit_id'], ['maintenance_units.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_staff_profiles_id'), 'staff_profiles', ['id'], unique=False)
    op.create_index(op.f('ix_staff_profiles_staff_number'), 'staff_profiles', ['staff_number'], unique=True)
    op.create_index(op.f('ix_staff_profiles_user_id'), 'staff_profiles', ['user_id'], unique=True)
    op.create_index(op.f('ix_staff_profiles_unit_id'), 'staff_profiles', ['unit_id'], unique=False)
    op.create_index(op.f('ix_staff_profiles_assigned_hostel_id'), 'staff_profiles', ['assigned_hostel_id'], unique=False)

    # 10. Create 'academic_sessions' table
    op.create_table(
        'academic_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_name', sa.String(length=50), nullable=False),
        sa.Column('semester', sa.String(length=20), server_default='first', nullable=False),
        sa.Column('is_current', sa.Boolean(), server_default='0', nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_name', 'semester', name='uq_session_semester')
    )
    op.create_index(op.f('ix_academic_sessions_id'), 'academic_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_academic_sessions_is_current'), 'academic_sessions', ['is_current'], unique=False)

    # 11. Create 'allocations' table
    op.create_table(
        'allocations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('bed_space_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), server_default='active', nullable=False),
        sa.Column('active_bed_marker', sa.Integer(), nullable=True),
        sa.Column('active_student_session_marker', sa.String(length=100), nullable=True),
        sa.Column('allocated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('expires_at', sa.DateTime(), nullable=True),
        sa.Column('checked_in_at', sa.DateTime(), nullable=True),
        sa.Column('checked_out_at', sa.DateTime(), nullable=True),
        sa.Column('allocated_by_user_id', sa.Integer(), nullable=True),
        sa.Column('notes', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['allocated_by_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['bed_space_id'], ['bed_spaces.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['session_id'], ['academic_sessions.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['student_id'], ['student_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('active_bed_marker', name='uq_active_bed_allocation'),
        sa.UniqueConstraint('active_student_session_marker', name='uq_active_student_session_allocation')
    )
    op.create_index(op.f('ix_allocations_id'), 'allocations', ['id'], unique=False)
    op.create_index(op.f('ix_allocations_student_id'), 'allocations', ['student_id'], unique=False)
    op.create_index(op.f('ix_allocations_bed_space_id'), 'allocations', ['bed_space_id'], unique=False)
    op.create_index(op.f('ix_allocations_session_id'), 'allocations', ['session_id'], unique=False)
    op.create_index(op.f('ix_allocations_status'), 'allocations', ['status'], unique=False)

    # 12. Create 'complaints' table
    op.create_table(
        'complaints',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('complaint_code', sa.String(length=50), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('room_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=30), nullable=False),
        sa.Column('urgency', sa.String(length=20), nullable=False),
        sa.Column('triage_source', sa.String(length=20), server_default='keyword', nullable=False),
        sa.Column('triage_confidence', sa.Float(), nullable=True),
        sa.Column('assigned_unit_id', sa.Integer(), nullable=False),
        sa.Column('assigned_officer_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=30), server_default='open', nullable=False),
        sa.Column('escalation_level', sa.Integer(), server_default='0', nullable=False),
        sa.Column('submitted_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('deadline_at', sa.DateTime(), nullable=False),
        sa.Column('escalated_to_warden_at', sa.DateTime(), nullable=True),
        sa.Column('escalated_to_admin_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('resolution_notes', sa.Text(), nullable=True),
        sa.Column('student_feedback_rating', sa.Integer(), nullable=True),
        sa.Column('student_feedback_comment', sa.Text(), nullable=True),
        sa.CheckConstraint('student_feedback_rating IS NULL OR (student_feedback_rating >= 1 AND student_feedback_rating <= 5)', name='chk_feedback_rating'),
        sa.CheckConstraint('escalation_level >= 0 AND escalation_level <= 2', name='chk_escalation_level'),
        sa.ForeignKeyConstraint(['assigned_officer_id'], ['staff_profiles.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['assigned_unit_id'], ['maintenance_units.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['student_profiles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_complaints_id'), 'complaints', ['id'], unique=False)
    op.create_index(op.f('ix_complaints_complaint_code'), 'complaints', ['complaint_code'], unique=True)
    op.create_index(op.f('ix_complaints_student_id'), 'complaints', ['student_id'], unique=False)
    op.create_index(op.f('ix_complaints_room_id'), 'complaints', ['room_id'], unique=False)
    op.create_index(op.f('ix_complaints_category'), 'complaints', ['category'], unique=False)
    op.create_index(op.f('ix_complaints_urgency'), 'complaints', ['urgency'], unique=False)
    op.create_index(op.f('ix_complaints_assigned_unit_id'), 'complaints', ['assigned_unit_id'], unique=False)
    op.create_index(op.f('ix_complaints_assigned_officer_id'), 'complaints', ['assigned_officer_id'], unique=False)
    op.create_index(op.f('ix_complaints_status'), 'complaints', ['status'], unique=False)
    op.create_index(op.f('ix_complaints_escalation_level'), 'complaints', ['escalation_level'], unique=False)
    op.create_index(op.f('ix_complaints_submitted_at'), 'complaints', ['submitted_at'], unique=False)
    op.create_index(op.f('ix_complaints_deadline_at'), 'complaints', ['deadline_at'], unique=False)
    op.create_index(op.f('ix_complaints_resolved_at'), 'complaints', ['resolved_at'], unique=False)
    op.create_index('ix_complaint_room_category_submitted', 'complaints', ['room_id', 'category', 'submitted_at'], unique=False)

    # 13. Create 'complaint_history' table
    op.create_table(
        'complaint_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('complaint_id', sa.Integer(), nullable=False),
        sa.Column('action_type', sa.String(length=50), nullable=False),
        sa.Column('from_status', sa.String(length=50), nullable=True),
        sa.Column('to_status', sa.String(length=50), nullable=True),
        sa.Column('from_escalation_level', sa.Integer(), nullable=True),
        sa.Column('to_escalation_level', sa.Integer(), nullable=True),
        sa.Column('performed_by_user_id', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['complaint_id'], ['complaints.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['performed_by_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_complaint_history_id'), 'complaint_history', ['id'], unique=False)
    op.create_index(op.f('ix_complaint_history_complaint_id'), 'complaint_history', ['complaint_id'], unique=False)
    op.create_index(op.f('ix_complaint_history_action_type'), 'complaint_history', ['action_type'], unique=False)
    op.create_index(op.f('ix_complaint_history_created_at'), 'complaint_history', ['created_at'], unique=False)
    op.create_index(op.f('ix_complaint_history_performed_by_user_id'), 'complaint_history', ['performed_by_user_id'], unique=False)

    # 14. Create 'notification_logs' table
    op.create_table(
        'notification_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipient_email', sa.String(length=100), nullable=False),
        sa.Column('recipient_role', sa.String(length=50), nullable=False),
        sa.Column('recipient_user_id', sa.Integer(), nullable=True),
        sa.Column('subject', sa.String(length=200), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('event_type', sa.String(length=50), nullable=False),
        sa.Column('complaint_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=20), server_default='sent', nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('sent_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['complaint_id'], ['complaints.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['recipient_user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_logs_id'), 'notification_logs', ['id'], unique=False)
    op.create_index(op.f('ix_notification_logs_recipient_email'), 'notification_logs', ['recipient_email'], unique=False)
    op.create_index(op.f('ix_notification_logs_event_type'), 'notification_logs', ['event_type'], unique=False)
    op.create_index(op.f('ix_notification_logs_status'), 'notification_logs', ['status'], unique=False)
    op.create_index(op.f('ix_notification_logs_sent_at'), 'notification_logs', ['sent_at'], unique=False)

    # 15. Create 'triage_keywords' table
    op.create_table(
        'triage_keywords',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('keyword', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=30), nullable=False),
        sa.Column('urgency', sa.String(length=20), nullable=False),
        sa.Column('weight', sa.Integer(), server_default='1', nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='1', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('keyword', 'category', name='uq_keyword_category')
    )
    op.create_index(op.f('ix_triage_keywords_id'), 'triage_keywords', ['id'], unique=False)
    op.create_index(op.f('ix_triage_keywords_keyword'), 'triage_keywords', ['keyword'], unique=False)
    op.create_index(op.f('ix_triage_keywords_category'), 'triage_keywords', ['category'], unique=False)
    op.create_index(op.f('ix_triage_keywords_urgency'), 'triage_keywords', ['urgency'], unique=False)

    # 16. Create 'audit_logs' table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('entity_name', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=True),
        sa.Column('old_values', sa.Text(), nullable=True),
        sa.Column('new_values', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_id'), 'audit_logs', ['id'], unique=False)
    op.create_index(op.f('ix_audit_logs_action'), 'audit_logs', ['action'], unique=False)
    op.create_index(op.f('ix_audit_logs_entity_name'), 'audit_logs', ['entity_name'], unique=False)
    op.create_index(op.f('ix_audit_logs_created_at'), 'audit_logs', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('triage_keywords')
    op.drop_table('notification_logs')
    op.drop_table('complaint_history')
    op.drop_table('complaints')
    op.drop_table('allocations')
    op.drop_table('academic_sessions')
    op.drop_table('staff_profiles')
    op.drop_table('student_profiles')
    op.drop_table('bed_spaces')
    op.drop_table('rooms')
    op.drop_table('hostels')
    op.drop_table('maintenance_units')
    op.drop_column('user_role', 'assigned_at')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    op.drop_column('roles', 'created_at')
    op.drop_column('roles', 'description')
