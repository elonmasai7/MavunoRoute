"""initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-05-21
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_role = sa.Enum(
        "SUPER_ADMIN",
        "OPS_ADMIN",
        "COOPERATIVE_ADMIN",
        "FARMER",
        "TRANSPORTER",
        "BUYER",
        "COLD_HUB_OPERATOR",
        "FINANCE_PARTNER",
        name="userrole",
    )
    verification_status = sa.Enum("PENDING", "VERIFIED", "REJECTED", name="verificationstatus")
    harvest_status = sa.Enum(
        "DRAFT",
        "READY",
        "MATCHED",
        "PICKUP_ASSIGNED",
        "IN_TRANSIT",
        "DELIVERED",
        "CANCELLED",
        name="harvestbatchstatus",
    )
    demand_status = sa.Enum("OPEN", "PARTIALLY_FULFILLED", "FULFILLED", "CANCELLED", name="buyerdemandstatus")
    route_status = sa.Enum("PLANNED", "ACTIVE", "COMPLETED", "CANCELLED", name="routestatus")
    pickup_status = sa.Enum("PENDING", "ACCEPTED", "PICKED", "REJECTED", "CANCELLED", name="pickupstatus")
    delivery_status = sa.Enum("PENDING", "IN_TRANSIT", "DELIVERED", "CANCELLED", name="deliverystatus")
    payment_status = sa.Enum("PENDING", "PROCESSING", "PAID", "FAILED", "CANCELLED", name="paymentstatus")

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=32), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone_number"),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_phone_number", "users", ["phone_number"])
    op.create_index("ix_users_role", "users", ["role"])

    op.create_table(
        "cooperatives",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("registration_number", sa.String(length=128), nullable=False),
        sa.Column("county", sa.String(length=128), nullable=False),
        sa.Column("contact_person", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=32), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("registration_number"),
    )

    op.create_table(
        "refresh_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("jti", sa.String(length=128), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("jti"),
    )

    op.create_table(
        "farmer_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("national_id_hash", sa.String(length=255), nullable=True),
        sa.Column("county", sa.String(length=128), nullable=False),
        sa.Column("sub_county", sa.String(length=128), nullable=False),
        sa.Column("ward", sa.String(length=128), nullable=False),
        sa.Column("village", sa.String(length=128), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("cooperative_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cooperatives.id"), nullable=True),
        sa.Column("farm_size_acres", sa.Float(), nullable=False),
        sa.Column("primary_crops", postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column("verification_status", verification_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "crops",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=False),
        sa.Column("perishability_level", sa.Integer(), nullable=False),
        sa.Column("ideal_temperature_min", sa.Float(), nullable=False),
        sa.Column("ideal_temperature_max", sa.Float(), nullable=False),
        sa.Column("shelf_life_hours", sa.Integer(), nullable=False),
        sa.Column("handling_notes", sa.String(length=500), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("name"),
    )

    op.create_table(
        "harvest_batches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("farmer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("farmer_profiles.id"), nullable=False),
        sa.Column("crop_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("crops.id"), nullable=False),
        sa.Column("quantity_kg", sa.Float(), nullable=False),
        sa.Column("expected_harvest_datetime", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actual_harvest_datetime", sa.DateTime(timezone=True), nullable=True),
        sa.Column("grade", sa.String(length=64), nullable=False),
        sa.Column("packaging_type", sa.String(length=64), nullable=False),
        sa.Column("asking_price_per_kg", sa.Float(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("status", harvest_status, nullable=False),
        sa.Column("spoilage_risk_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "buyer_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("business_name", sa.String(length=255), nullable=False),
        sa.Column("business_type", sa.String(length=128), nullable=False),
        sa.Column("kra_pin", sa.String(length=32), nullable=True),
        sa.Column("county", sa.String(length=128), nullable=False),
        sa.Column("delivery_address", sa.String(length=255), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("verification_status", verification_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "buyer_demands",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("buyer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("buyer_profiles.id"), nullable=False),
        sa.Column("crop_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("crops.id"), nullable=False),
        sa.Column("quantity_kg", sa.Float(), nullable=False),
        sa.Column("desired_grade", sa.String(length=64), nullable=False),
        sa.Column("max_price_per_kg", sa.Float(), nullable=False),
        sa.Column("required_delivery_datetime", sa.DateTime(timezone=True), nullable=False),
        sa.Column("delivery_latitude", sa.Float(), nullable=False),
        sa.Column("delivery_longitude", sa.Float(), nullable=False),
        sa.Column("status", demand_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "transporter_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("business_name", sa.String(length=255), nullable=False),
        sa.Column("license_number", sa.String(length=128), nullable=False),
        sa.Column("phone_number", sa.String(length=32), nullable=False),
        sa.Column("county", sa.String(length=128), nullable=False),
        sa.Column("verification_status", verification_status, nullable=False),
        sa.Column("rating", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id"),
        sa.UniqueConstraint("license_number"),
    )

    op.create_table(
        "vehicles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("transporter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("transporter_profiles.id"), nullable=False),
        sa.Column("plate_number", sa.String(length=32), nullable=False),
        sa.Column("vehicle_type", sa.String(length=64), nullable=False),
        sa.Column("capacity_kg", sa.Float(), nullable=False),
        sa.Column("has_refrigeration", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("temperature_min", sa.Float(), nullable=True),
        sa.Column("temperature_max", sa.Float(), nullable=True),
        sa.Column("insurance_status", sa.String(length=64), nullable=False),
        sa.Column("inspection_status", sa.String(length=64), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("plate_number"),
    )

    op.create_table(
        "cold_hubs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("operator_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("county", sa.String(length=128), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("total_capacity_kg", sa.Float(), nullable=False),
        sa.Column("available_capacity_kg", sa.Float(), nullable=False),
        sa.Column("temperature_min", sa.Float(), nullable=False),
        sa.Column("temperature_max", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "route_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("route_code", sa.String(length=64), nullable=False),
        sa.Column("origin_county", sa.String(length=128), nullable=False),
        sa.Column("destination_county", sa.String(length=128), nullable=False),
        sa.Column("vehicle_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("vehicles.id"), nullable=True),
        sa.Column("transporter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("transporter_profiles.id"), nullable=True),
        sa.Column("assigned_driver_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("total_distance_km", sa.Float(), nullable=False),
        sa.Column("estimated_duration_minutes", sa.Integer(), nullable=False),
        sa.Column("route_polyline", sa.String(), nullable=True),
        sa.Column("route_provider", sa.String(length=64), nullable=False),
        sa.Column("status", route_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("route_code"),
    )

    op.create_table(
        "route_stops",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("route_plan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("route_plans.id"), nullable=False),
        sa.Column("stop_type", sa.String(length=32), nullable=False),
        sa.Column("farmer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("farmer_profiles.id"), nullable=True),
        sa.Column("buyer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("buyer_profiles.id"), nullable=True),
        sa.Column("cold_hub_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cold_hubs.id"), nullable=True),
        sa.Column("harvest_batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("harvest_batches.id"), nullable=True),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("planned_arrival_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("actual_arrival_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "transport_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("route_plan_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("route_plans.id"), nullable=False),
        sa.Column("harvest_batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("harvest_batches.id"), nullable=False),
        sa.Column("buyer_demand_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("buyer_demands.id"), nullable=True),
        sa.Column("transporter_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("transporter_profiles.id"), nullable=False),
        sa.Column("vehicle_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("vehicles.id"), nullable=False),
        sa.Column("pickup_status", pickup_status, nullable=False),
        sa.Column("delivery_status", delivery_status, nullable=False),
        sa.Column("agreed_transport_fee", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "proof_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("transport_job_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("transport_jobs.id"), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("qr_code", sa.String(length=128), nullable=False),
        sa.Column("photo_url", sa.String(length=500), nullable=True),
        sa.Column("signature_url", sa.String(length=500), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("recorded_by_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("notes", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("qr_code"),
    )

    op.create_table(
        "temperature_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("harvest_batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("harvest_batches.id"), nullable=False),
        sa.Column("transport_job_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("transport_jobs.id"), nullable=True),
        sa.Column("cold_hub_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cold_hubs.id"), nullable=True),
        sa.Column("temperature_celsius", sa.Float(), nullable=False),
        sa.Column("humidity", sa.Float(), nullable=True),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("payer_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("payee_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("related_transport_job_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("transport_jobs.id"), nullable=True),
        sa.Column("related_harvest_batch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("harvest_batches.id"), nullable=True),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=8), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("provider_reference", sa.String(length=255), nullable=True),
        sa.Column("status", payment_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "mpesa_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("payment_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("payments.id"), nullable=False),
        sa.Column("checkout_request_id", sa.String(length=255), nullable=False),
        sa.Column("merchant_request_id", sa.String(length=255), nullable=False),
        sa.Column("phone_number", sa.String(length=32), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("result_code", sa.String(length=32), nullable=True),
        sa.Column("result_description", sa.String(length=255), nullable=True),
        sa.Column("provider_payload_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("checkout_request_id"),
    )

    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("message", sa.String(length=500), nullable=False),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("provider_reference", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.String(length=64), nullable=False),
        sa.Column("ip_address", sa.String(length=64), nullable=False),
        sa.Column("user_agent", sa.String(length=500), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "api_integration_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("provider", sa.String(length=64), nullable=False),
        sa.Column("request_type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("response_code", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("api_integration_logs")
    op.drop_table("audit_logs")
    op.drop_table("notifications")
    op.drop_table("mpesa_transactions")
    op.drop_table("payments")
    op.drop_table("temperature_events")
    op.drop_table("proof_events")
    op.drop_table("transport_jobs")
    op.drop_table("route_stops")
    op.drop_table("route_plans")
    op.drop_table("cold_hubs")
    op.drop_table("vehicles")
    op.drop_table("transporter_profiles")
    op.drop_table("buyer_demands")
    op.drop_table("buyer_profiles")
    op.drop_table("harvest_batches")
    op.drop_table("crops")
    op.drop_table("farmer_profiles")
    op.drop_table("refresh_tokens")
    op.drop_table("cooperatives")
    op.drop_table("users")

    bind = op.get_bind()
    sa.Enum(name="paymentstatus").drop(bind, checkfirst=True)
    sa.Enum(name="deliverystatus").drop(bind, checkfirst=True)
    sa.Enum(name="pickupstatus").drop(bind, checkfirst=True)
    sa.Enum(name="routestatus").drop(bind, checkfirst=True)
    sa.Enum(name="buyerdemandstatus").drop(bind, checkfirst=True)
    sa.Enum(name="harvestbatchstatus").drop(bind, checkfirst=True)
    sa.Enum(name="verificationstatus").drop(bind, checkfirst=True)
    sa.Enum(name="userrole").drop(bind, checkfirst=True)
