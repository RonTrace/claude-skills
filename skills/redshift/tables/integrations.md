# External Integration Tables

## hubspot.deals
HubSpot CRM deals with Trace-specific properties.

**Common Columns:**
- `dealid` - HubSpot deal ID (primary key)
- `property_trace_division_id__value` - Links to Trace division_id
- `property_stripe_customer_id__value` - Stripe customer ID
- `property_hs_is_closed_lost__value` - 'true' if deal is closed lost
- `property_hs_is_closed_lost__timestamp` - When deal was closed lost
- `property_equipment_return_status__value` - Equipment return status
- `property_fedex_tracking_number__churn___value` - FedEx tracking for returns
- `property_fedex_return_label__value` - FedEx return label
- `property_dealstage__value` - Current deal stage
- `property_dealtype__value` - Deal type
- `property_pipeline__value` - Pipeline

**Find closed lost deals with Trace division:**
```sql
SELECT
    dealid,
    property_trace_division_id__value AS division_id,
    property_equipment_return_status__value AS return_status,
    property_hs_is_closed_lost__timestamp AS closed_date
FROM hubspot.deals
WHERE property_hs_is_closed_lost__value = 'true'
    AND property_trace_division_id__value IS NOT NULL
ORDER BY property_hs_is_closed_lost__timestamp DESC
```

---

## shipstation.shipments
ShipStation shipping records.

**Common Columns:**
- `createdate` - When shipment was created
- Tracking and shipment info

```sql
SELECT * FROM shipstation.shipments ORDER BY createdate DESC LIMIT 100
```
