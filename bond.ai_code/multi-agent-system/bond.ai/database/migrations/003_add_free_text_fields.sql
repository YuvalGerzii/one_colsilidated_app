-- Add free text fields for looking_for and can_offer
-- This allows users to provide additional details beyond the predefined options

ALTER TABLE user_registration_data
ADD COLUMN IF NOT EXISTS looking_for_details TEXT,
ADD COLUMN IF NOT EXISTS can_offer_details TEXT;

-- Add comments for documentation
COMMENT ON COLUMN user_registration_data.looking_for_details IS 'Additional free text details about what the user is looking for';
COMMENT ON COLUMN user_registration_data.can_offer_details IS 'Additional free text details about what the user can offer';
