/**
 * Enhanced Registration Routes
 * Handles comprehensive user registration data including skills, experience, and professional information
 */

import express, { Response } from 'express';
import { AuthRequest, authenticateToken } from '../auth/jwt';
import { getDb } from '../database/connection';

const router = express.Router();

/**
 * Complete enhanced registration
 * POST /api/registration/complete
 */
router.post('/complete', authenticateToken, async (req: AuthRequest, res: Response) => {
  try {
    const userId = req.user?.userId;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const {
      // Step 1: Basic Information
      fullName,
      email,
      phone,
      country,
      city,

      // Step 2: Professional Information
      jobTitle,
      company,
      industry,
      yearsExperience,
      companySize,

      // Step 3: Skills & Expertise
      technicalSkills,
      softSkills,
      domainExpertise,

      // Step 4: Goals & Preferences
      lookingFor,
      lookingForDetails,
      canOffer,
      canOfferDetails,
      professionalGoals,
      timeCommitment,

      // Step 5: Matching Preferences
      urgency,
      timeline,
      relationshipType,
      communicationStyle,
      workingStyle,
      geographicPreference,
      preferredIndustries,
      budgetRange,
      dealBreakers,
      successCriteria,
      pastCollaborationExperience,
      specificChallenges,

      // Optional fields
      bio,
      linkedinUrl,
      portfolioUrl,
      twitterUrl,
      githubUrl,
    } = req.body;

    const db = getDb();

    // Start transaction
    await db.transaction(async (client) => {
      // Update users table
      await client.query(
        `UPDATE users
         SET full_name = $1,
             phone_number = $2,
             country = $3,
             city = $4,
             industry = $5,
             onboarding_completed = true,
             profile_completion_percentage = 100,
             updated_at = NOW()
         WHERE id = $6`,
        [fullName, phone, country, city, industry, userId]
      );

      // Update user_profiles table
      await client.query(
        `INSERT INTO user_profiles (
          user_id,
          bio,
          job_title,
          company,
          skills,
          looking_for,
          can_help_with,
          created_at,
          updated_at
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, NOW(), NOW())
        ON CONFLICT (user_id)
        DO UPDATE SET
          bio = $2,
          job_title = $3,
          company = $4,
          skills = $5,
          looking_for = $6,
          can_help_with = $7,
          updated_at = NOW()`,
        [
          userId,
          bio || '',
          jobTitle,
          company,
          JSON.stringify(technicalSkills),
          lookingFor,
          canOffer,
        ]
      );

      // Insert/Update user_registration_data table
      await client.query(
        `INSERT INTO user_registration_data (
          user_id,
          full_name,
          email,
          phone_number,
          country,
          city,
          current_job_title,
          current_company,
          industry,
          years_of_experience,
          company_size,
          technical_skills,
          soft_skills,
          domain_expertise,
          looking_for,
          looking_for_details,
          can_offer,
          can_offer_details,
          professional_goals,
          time_commitment,
          urgency,
          timeline,
          relationship_type,
          communication_style,
          working_style,
          geographic_preference,
          preferred_industries,
          budget_range,
          deal_breakers,
          success_criteria,
          past_collaboration_experience,
          specific_challenges,
          bio,
          linkedin_url,
          twitter_url,
          github_url,
          portfolio_url,
          completed_at,
          created_at,
          updated_at
        ) VALUES (
          $1, $2, $3, $4, $5, $6, $7, $8, $9, $10,
          $11, $12, $13, $14, $15, $16, $17, $18, $19, $20,
          $21, $22, $23, $24, $25, $26, $27, $28, $29, $30,
          $31, $32, $33, $34, $35, $36, $37, NOW(), NOW(), NOW()
        )
        ON CONFLICT (user_id)
        DO UPDATE SET
          full_name = $2,
          email = $3,
          phone_number = $4,
          country = $5,
          city = $6,
          current_job_title = $7,
          current_company = $8,
          industry = $9,
          years_of_experience = $10,
          company_size = $11,
          technical_skills = $12,
          soft_skills = $13,
          domain_expertise = $14,
          looking_for = $15,
          looking_for_details = $16,
          can_offer = $17,
          can_offer_details = $18,
          professional_goals = $19,
          time_commitment = $20,
          urgency = $21,
          timeline = $22,
          relationship_type = $23,
          communication_style = $24,
          working_style = $25,
          geographic_preference = $26,
          preferred_industries = $27,
          budget_range = $28,
          deal_breakers = $29,
          success_criteria = $30,
          past_collaboration_experience = $31,
          specific_challenges = $32,
          bio = $33,
          linkedin_url = $34,
          twitter_url = $35,
          github_url = $36,
          portfolio_url = $37,
          completed_at = NOW(),
          updated_at = NOW()`,
        [
          userId,
          fullName,
          email,
          phone || null,
          country,
          city,
          jobTitle,
          company,
          industry,
          yearsExperience || 0,
          companySize,
          JSON.stringify(technicalSkills),
          JSON.stringify(softSkills),
          domainExpertise,
          lookingFor,
          lookingForDetails || null,
          canOffer,
          canOfferDetails || null,
          professionalGoals || '',
          timeCommitment,
          urgency,
          timeline,
          relationshipType,
          communicationStyle,
          workingStyle,
          geographicPreference,
          preferredIndustries || null,
          budgetRange || null,
          dealBreakers || null,
          successCriteria,
          pastCollaborationExperience || null,
          specificChallenges || null,
          bio || '',
          linkedinUrl || null,
          twitterUrl || null,
          githubUrl || null,
          portfolioUrl || null,
        ]
      );
    });

    // Fetch complete user profile
    const profile = await db.queryOne(
      `SELECT * FROM complete_user_profiles WHERE user_id = $1`,
      [userId]
    );

    res.json({
      success: true,
      message: 'Registration completed successfully',
      profile,
    });
  } catch (error: any) {
    console.error('Enhanced registration error:', error);
    res.status(500).json({ error: 'Failed to complete registration' });
  }
});

/**
 * Get registration progress
 * GET /api/registration/progress
 */
router.get('/progress', authenticateToken, async (req: AuthRequest, res: Response) => {
  try {
    const userId = req.user?.userId;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const db = getDb();

    // Get user registration data
    const registrationData = await db.queryOne(
      `SELECT
        full_name,
        phone_number,
        country,
        city,
        current_job_title,
        current_company,
        industry,
        years_of_experience,
        company_size,
        technical_skills,
        soft_skills,
        domain_expertise,
        looking_for,
        looking_for_details,
        can_offer,
        can_offer_details,
        professional_goals,
        time_commitment,
        urgency,
        timeline,
        relationship_type,
        communication_style,
        working_style,
        geographic_preference,
        preferred_industries,
        budget_range,
        deal_breakers,
        success_criteria,
        past_collaboration_experience,
        specific_challenges,
        bio,
        linkedin_url,
        portfolio_url,
        twitter_url,
        github_url,
        completed_at
       FROM user_registration_data
       WHERE user_id = $1`,
      [userId]
    );

    // Calculate completion percentage
    let completionPercentage = 0;
    if (registrationData) {
      const fields = [
        'full_name',
        'country',
        'city',
        'current_job_title',
        'current_company',
        'industry',
        'technical_skills',
        'soft_skills',
        'looking_for',
        'can_offer',
      ];

      const completedFields = fields.filter(
        (field) => registrationData[field] && registrationData[field] !== ''
      );
      completionPercentage = Math.round((completedFields.length / fields.length) * 100);
    }

    res.json({
      registrationData: registrationData || null,
      completionPercentage,
      isCompleted: !!registrationData?.completed_at,
    });
  } catch (error: any) {
    console.error('Get registration progress error:', error);
    res.status(500).json({ error: 'Failed to get registration progress' });
  }
});

/**
 * Update partial registration data
 * PATCH /api/registration/update
 */
router.patch('/update', authenticateToken, async (req: AuthRequest, res: Response) => {
  try {
    const userId = req.user?.userId;
    if (!userId) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const updates = req.body;
    const db = getDb();

    // Build dynamic update query
    const updateFields = Object.keys(updates)
      .filter((key) => updates[key] !== undefined)
      .map((key, index) => `${key} = $${index + 2}`)
      .join(', ');

    if (!updateFields) {
      return res.status(400).json({ error: 'No fields to update' });
    }

    const values = Object.keys(updates)
      .filter((key) => updates[key] !== undefined)
      .map((key) => {
        const value = updates[key];
        // Convert arrays and objects to JSON
        if (Array.isArray(value) || typeof value === 'object') {
          return JSON.stringify(value);
        }
        return value;
      });

    await db.query(
      `UPDATE user_registration_data
       SET ${updateFields}, updated_at = NOW()
       WHERE user_id = $1`,
      [userId, ...values]
    );

    res.json({
      success: true,
      message: 'Registration data updated successfully',
    });
  } catch (error: any) {
    console.error('Update registration error:', error);
    res.status(500).json({ error: 'Failed to update registration data' });
  }
});

export default router;
