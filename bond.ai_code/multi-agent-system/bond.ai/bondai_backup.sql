--
-- PostgreSQL database dump
--

\restrict 5qfok7oogB6N8zmX8elOHaSIkoiQBj8G5e0b1DQrhg963HrQkpJa9d3XOMSabqv

-- Dumped from database version 15.14
-- Dumped by pg_dump version 15.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_updated_at_column() OWNER TO postgres;

--
-- Name: update_user_registration_updated_at(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_user_registration_updated_at() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_user_registration_updated_at() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activity_log (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    activity_type character varying(100) NOT NULL,
    entity_type character varying(50),
    entity_id uuid,
    metadata jsonb,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.activity_log OWNER TO postgres;

--
-- Name: user_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_profiles (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    bio text,
    job_title character varying(255),
    company character varying(255),
    linkedin_url character varying(500),
    twitter_url character varying(500),
    website_url character varying(500),
    location jsonb,
    expertise_areas text[],
    needs text[],
    offers text[],
    years_experience integer,
    education jsonb[],
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    skills jsonb DEFAULT '[]'::jsonb,
    interests jsonb DEFAULT '[]'::jsonb,
    looking_for text[],
    can_help_with text[],
    industry_sectors text[],
    company_size character varying(50),
    availability character varying(50),
    communication_style character varying(50),
    goals jsonb DEFAULT '[]'::jsonb,
    certifications jsonb DEFAULT '[]'::jsonb,
    languages jsonb DEFAULT '[]'::jsonb,
    preferred_connection_types text[],
    achievements text[],
    current_projects jsonb DEFAULT '[]'::jsonb
);


ALTER TABLE public.user_profiles OWNER TO postgres;

--
-- Name: user_registration_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_registration_data (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    full_name character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    phone_number character varying(50),
    date_of_birth date,
    gender character varying(50),
    country character varying(100),
    city character varying(100),
    state_province character varying(100),
    postal_code character varying(20),
    timezone character varying(100),
    current_job_title character varying(255),
    current_company character varying(255),
    industry character varying(100),
    years_of_experience integer,
    company_size character varying(50),
    employment_type character varying(50),
    technical_skills jsonb DEFAULT '[]'::jsonb,
    soft_skills jsonb DEFAULT '[]'::jsonb,
    domain_expertise text[],
    looking_for text[],
    can_offer text[],
    professional_goals text,
    time_commitment character varying(50),
    preferred_communication_styles text[],
    preferred_meeting_times character varying(100),
    willing_to_travel boolean DEFAULT false,
    remote_preference character varying(50),
    education jsonb DEFAULT '[]'::jsonb,
    certifications jsonb DEFAULT '[]'::jsonb,
    languages jsonb DEFAULT '[]'::jsonb,
    bio text,
    website_url character varying(500),
    linkedin_url character varying(500),
    twitter_url character varying(500),
    github_url character varying(500),
    portfolio_url character varying(500),
    registration_source character varying(100),
    referral_code character varying(100),
    marketing_consent boolean DEFAULT false,
    terms_accepted boolean DEFAULT true,
    privacy_accepted boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    completed_at timestamp without time zone
);


ALTER TABLE public.user_registration_data OWNER TO postgres;

--
-- Name: TABLE user_registration_data; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.user_registration_data IS 'Comprehensive user registration data including skills, preferences, and professional information';


--
-- Name: COLUMN user_registration_data.technical_skills; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_registration_data.technical_skills IS 'JSON array of technical skills with proficiency levels and experience';


--
-- Name: COLUMN user_registration_data.looking_for; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_registration_data.looking_for IS 'Array of what the user is seeking (mentorship, partnerships, etc.)';


--
-- Name: COLUMN user_registration_data.can_offer; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.user_registration_data.can_offer IS 'Array of what the user can provide to others';


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    email character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    password_hash character varying(255),
    industry character varying(100),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    last_login timestamp without time zone,
    is_active boolean DEFAULT true,
    verification_token character varying(255),
    verified boolean DEFAULT false,
    full_name character varying(255),
    phone_number character varying(50),
    country character varying(100),
    city character varying(100),
    timezone character varying(100),
    preferred_language character varying(10) DEFAULT 'en'::character varying,
    avatar_url character varying(500),
    onboarding_completed boolean DEFAULT false,
    profile_completion_percentage integer DEFAULT 0
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: complete_user_profiles; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.complete_user_profiles AS
 SELECT u.id AS user_id,
    u.email,
    u.full_name,
    u.industry,
    u.created_at AS user_created_at,
    u.is_active,
    u.onboarding_completed,
    u.profile_completion_percentage,
    up.bio,
    up.job_title,
    up.company,
    up.skills,
    up.interests,
    up.looking_for,
    up.can_help_with,
    urd.current_job_title,
    urd.years_of_experience,
    urd.technical_skills,
    urd.soft_skills,
    urd.professional_goals,
    urd.linkedin_url,
    urd.portfolio_url
   FROM ((public.users u
     LEFT JOIN public.user_profiles up ON ((u.id = up.user_id)))
     LEFT JOIN public.user_registration_data urd ON ((u.id = urd.user_id)));


ALTER TABLE public.complete_user_profiles OWNER TO postgres;

--
-- Name: connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.connections (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    contact_id uuid,
    strength numeric(3,2) DEFAULT 0.5,
    trust_level numeric(3,2) DEFAULT 0.5,
    last_interaction timestamp without time zone,
    interaction_count integer DEFAULT 0,
    notes text,
    tags text[],
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.connections OWNER TO postgres;

--
-- Name: contacts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contacts (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    email character varying(255) NOT NULL,
    name character varying(255),
    company character varying(255),
    job_title character varying(255),
    source character varying(50),
    imported_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    metadata jsonb
);


ALTER TABLE public.contacts OWNER TO postgres;

--
-- Name: cross_tier_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cross_tier_requests (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    requester_id uuid,
    target_id uuid,
    value_proposition_id uuid,
    requester_tier character varying(50) NOT NULL,
    target_tier character varying(50) NOT NULL,
    tier_gap integer NOT NULL,
    gatekeeper_passed boolean NOT NULL,
    gatekeeper_score integer NOT NULL,
    required_threshold integer NOT NULL,
    vp_strength_score integer,
    specificity_score integer,
    relevance_score integer,
    professionalism_score integer,
    mutual_benefit_score integer,
    verification_score integer,
    recommendation text,
    warnings text[],
    approved boolean NOT NULL,
    approval_reason text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_gatekeeper_score CHECK (((gatekeeper_score >= 0) AND (gatekeeper_score <= 100))),
    CONSTRAINT check_tier_gap CHECK ((tier_gap >= 0))
);


ALTER TABLE public.cross_tier_requests OWNER TO postgres;

--
-- Name: TABLE cross_tier_requests; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.cross_tier_requests IS 'Cross-tier access requests with gatekeeper validation results';


--
-- Name: enhanced_matches; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.enhanced_matches (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    seeker_id uuid,
    target_id uuid,
    seeker_tier character varying(50) NOT NULL,
    target_tier character varying(50) NOT NULL,
    tier_gap integer NOT NULL,
    appropriate_match boolean NOT NULL,
    requires_gatekeeper boolean NOT NULL,
    value_proposition_id uuid,
    seeker_benefit integer NOT NULL,
    target_benefit integer NOT NULL,
    mutuality_score integer NOT NULL,
    balance_ratio numeric(3,2) NOT NULL,
    imbalance_warning boolean DEFAULT false,
    needs_alignment integer,
    urgency_alignment integer,
    scope_alignment integer,
    resource_alignment integer,
    timing_alignment integer,
    domain_alignment integer,
    overall_alignment integer,
    compatibility_score numeric(3,2) NOT NULL,
    value_potential numeric(3,2) NOT NULL,
    success_probability numeric(3,2) NOT NULL,
    overall_score numeric(3,2) NOT NULL,
    match_type character varying(50) NOT NULL,
    priority character varying(50) NOT NULL,
    status character varying(50) DEFAULT 'new'::character varying,
    seeker_needs_addressed text[],
    target_needs_addressed text[],
    match_reasons jsonb,
    shortest_path_length integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    dismissed_at timestamp without time zone,
    CONSTRAINT check_balance_ratio CHECK (((balance_ratio >= (0)::numeric) AND (balance_ratio <= (1)::numeric))),
    CONSTRAINT check_mutuality_score CHECK (((mutuality_score >= 0) AND (mutuality_score <= 100))),
    CONSTRAINT check_tier_gap_matches CHECK ((tier_gap >= 0))
);


ALTER TABLE public.enhanced_matches OWNER TO postgres;

--
-- Name: TABLE enhanced_matches; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.enhanced_matches IS 'Tier-aware matches with bidirectional validation and contextual alignment';


--
-- Name: COLUMN enhanced_matches.mutuality_score; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.enhanced_matches.mutuality_score IS 'Minimum of seeker_benefit and target_benefit - both must benefit';


--
-- Name: COLUMN enhanced_matches.balance_ratio; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.enhanced_matches.balance_ratio IS 'Ratio of min to max benefit - should be close to 1.0 for balanced exchange';


--
-- Name: introductions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.introductions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    introducer_id uuid,
    person1_id uuid,
    person2_id uuid,
    message_id uuid,
    status character varying(50) DEFAULT 'pending'::character varying,
    person1_accepted boolean,
    person2_accepted boolean,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    accepted_at timestamp without time zone,
    completed_at timestamp without time zone,
    outcome text,
    metadata jsonb
);


ALTER TABLE public.introductions OWNER TO postgres;

--
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.messages (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    sender_id uuid,
    recipient_id uuid,
    subject character varying(500),
    body text NOT NULL,
    sent_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    read_at timestamp without time zone,
    thread_id uuid,
    metadata jsonb,
    is_introduction boolean DEFAULT false
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- Name: network_snapshots; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.network_snapshots (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    total_connections integer NOT NULL,
    avg_trust_level numeric(3,2),
    degree_centrality numeric(5,4),
    betweenness_centrality numeric(5,4),
    page_rank numeric(5,4),
    clustering_coefficient numeric(5,4),
    community_count integer,
    network_density numeric(5,4)
);


ALTER TABLE public.network_snapshots OWNER TO postgres;

--
-- Name: opportunities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.opportunities (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    type character varying(50) NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    target_user_ids uuid[],
    score integer,
    confidence numeric(3,2),
    status character varying(50) DEFAULT 'active'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    expires_at timestamp without time zone,
    metadata jsonb
);


ALTER TABLE public.opportunities OWNER TO postgres;

--
-- Name: relationship_health_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.relationship_health_history (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    target_user_id uuid,
    health_score integer NOT NULL,
    category character varying(50) NOT NULL,
    metrics jsonb NOT NULL,
    risks jsonb,
    opportunities jsonb,
    recorded_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.relationship_health_history OWNER TO postgres;

--
-- Name: tier_profiles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tier_profiles (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    user_id uuid,
    contact_id uuid,
    tier character varying(50) NOT NULL,
    tier_score integer NOT NULL,
    career_years integer,
    seniority_level integer,
    achievement_score integer,
    industry_authority integer,
    organization_level integer,
    network_size integer DEFAULT 0,
    follower_count integer DEFAULT 0,
    publications_count integer DEFAULT 0,
    speaking_engagements integer DEFAULT 0,
    awards_recognitions integer DEFAULT 0,
    media_presence integer DEFAULT 0,
    verified boolean DEFAULT false,
    verification_sources text[],
    verified_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_org_level CHECK (((organization_level >= 1) AND (organization_level <= 10))),
    CONSTRAINT check_seniority_level CHECK (((seniority_level >= 1) AND (seniority_level <= 10))),
    CONSTRAINT check_tier_score CHECK (((tier_score >= 0) AND (tier_score <= 100)))
);


ALTER TABLE public.tier_profiles OWNER TO postgres;

--
-- Name: TABLE tier_profiles; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.tier_profiles IS 'Professional tier classification for users and contacts based on career stage, influence, and achievements';


--
-- Name: COLUMN tier_profiles.tier; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.tier_profiles.tier IS 'Professional tier: entry, junior, mid_level, senior, executive, c_level, founder_ceo, luminary';


--
-- Name: value_propositions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.value_propositions (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    proposer_id uuid,
    target_id uuid,
    category character varying(50) NOT NULL,
    description text NOT NULL,
    strength integer NOT NULL,
    specificity integer NOT NULL,
    verifiability integer NOT NULL,
    uniqueness integer NOT NULL,
    timeliness integer NOT NULL,
    evidence text[],
    needs_addressed text[],
    validated boolean DEFAULT false,
    validated_at timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_specificity CHECK (((specificity >= 0) AND (specificity <= 100))),
    CONSTRAINT check_strength CHECK (((strength >= 0) AND (strength <= 100)))
);


ALTER TABLE public.value_propositions OWNER TO postgres;

--
-- Name: TABLE value_propositions; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE public.value_propositions IS 'Value propositions from seekers to targets, assessed for strength and relevance';


--
-- Data for Name: activity_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.activity_log (id, user_id, activity_type, entity_type, entity_id, metadata, created_at) FROM stdin;
\.


--
-- Data for Name: connections; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.connections (id, user_id, contact_id, strength, trust_level, last_interaction, interaction_count, notes, tags, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: contacts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contacts (id, user_id, email, name, company, job_title, source, imported_at, metadata) FROM stdin;
\.


--
-- Data for Name: cross_tier_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cross_tier_requests (id, requester_id, target_id, value_proposition_id, requester_tier, target_tier, tier_gap, gatekeeper_passed, gatekeeper_score, required_threshold, vp_strength_score, specificity_score, relevance_score, professionalism_score, mutual_benefit_score, verification_score, recommendation, warnings, approved, approval_reason, created_at) FROM stdin;
\.


--
-- Data for Name: enhanced_matches; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.enhanced_matches (id, seeker_id, target_id, seeker_tier, target_tier, tier_gap, appropriate_match, requires_gatekeeper, value_proposition_id, seeker_benefit, target_benefit, mutuality_score, balance_ratio, imbalance_warning, needs_alignment, urgency_alignment, scope_alignment, resource_alignment, timing_alignment, domain_alignment, overall_alignment, compatibility_score, value_potential, success_probability, overall_score, match_type, priority, status, seeker_needs_addressed, target_needs_addressed, match_reasons, shortest_path_length, created_at, updated_at, dismissed_at) FROM stdin;
\.


--
-- Data for Name: introductions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.introductions (id, introducer_id, person1_id, person2_id, message_id, status, person1_accepted, person2_accepted, created_at, accepted_at, completed_at, outcome, metadata) FROM stdin;
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.messages (id, sender_id, recipient_id, subject, body, sent_at, read_at, thread_id, metadata, is_introduction) FROM stdin;
\.


--
-- Data for Name: network_snapshots; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.network_snapshots (id, user_id, "timestamp", total_connections, avg_trust_level, degree_centrality, betweenness_centrality, page_rank, clustering_coefficient, community_count, network_density) FROM stdin;
\.


--
-- Data for Name: opportunities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.opportunities (id, user_id, type, title, description, target_user_ids, score, confidence, status, created_at, updated_at, expires_at, metadata) FROM stdin;
\.


--
-- Data for Name: relationship_health_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.relationship_health_history (id, user_id, target_user_id, health_score, category, metrics, risks, opportunities, recorded_at) FROM stdin;
\.


--
-- Data for Name: tier_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tier_profiles (id, user_id, contact_id, tier, tier_score, career_years, seniority_level, achievement_score, industry_authority, organization_level, network_size, follower_count, publications_count, speaking_engagements, awards_recognitions, media_presence, verified, verification_sources, verified_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user_profiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_profiles (id, user_id, bio, job_title, company, linkedin_url, twitter_url, website_url, location, expertise_areas, needs, offers, years_experience, education, created_at, updated_at, skills, interests, looking_for, can_help_with, industry_sectors, company_size, availability, communication_style, goals, certifications, languages, preferred_connection_types, achievements, current_projects) FROM stdin;
\.


--
-- Data for Name: user_registration_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_registration_data (id, user_id, full_name, email, phone_number, date_of_birth, gender, country, city, state_province, postal_code, timezone, current_job_title, current_company, industry, years_of_experience, company_size, employment_type, technical_skills, soft_skills, domain_expertise, looking_for, can_offer, professional_goals, time_commitment, preferred_communication_styles, preferred_meeting_times, willing_to_travel, remote_preference, education, certifications, languages, bio, website_url, linkedin_url, twitter_url, github_url, portfolio_url, registration_source, referral_code, marketing_consent, terms_accepted, privacy_accepted, created_at, updated_at, completed_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, name, password_hash, industry, created_at, updated_at, last_login, is_active, verification_token, verified, full_name, phone_number, country, city, timezone, preferred_language, avatar_url, onboarding_completed, profile_completion_percentage) FROM stdin;
\.


--
-- Data for Name: value_propositions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.value_propositions (id, proposer_id, target_id, category, description, strength, specificity, verifiability, uniqueness, timeliness, evidence, needs_addressed, validated, validated_at, created_at, updated_at) FROM stdin;
\.


--
-- Name: activity_log activity_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_log
    ADD CONSTRAINT activity_log_pkey PRIMARY KEY (id);


--
-- Name: connections connections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_pkey PRIMARY KEY (id);


--
-- Name: connections connections_user_id_contact_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_user_id_contact_id_key UNIQUE (user_id, contact_id);


--
-- Name: contacts contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_pkey PRIMARY KEY (id);


--
-- Name: cross_tier_requests cross_tier_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cross_tier_requests
    ADD CONSTRAINT cross_tier_requests_pkey PRIMARY KEY (id);


--
-- Name: enhanced_matches enhanced_matches_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enhanced_matches
    ADD CONSTRAINT enhanced_matches_pkey PRIMARY KEY (id);


--
-- Name: introductions introductions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.introductions
    ADD CONSTRAINT introductions_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: network_snapshots network_snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.network_snapshots
    ADD CONSTRAINT network_snapshots_pkey PRIMARY KEY (id);


--
-- Name: network_snapshots network_snapshots_user_id_timestamp_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.network_snapshots
    ADD CONSTRAINT network_snapshots_user_id_timestamp_key UNIQUE (user_id, "timestamp");


--
-- Name: opportunities opportunities_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunities
    ADD CONSTRAINT opportunities_pkey PRIMARY KEY (id);


--
-- Name: relationship_health_history relationship_health_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relationship_health_history
    ADD CONSTRAINT relationship_health_history_pkey PRIMARY KEY (id);


--
-- Name: tier_profiles tier_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tier_profiles
    ADD CONSTRAINT tier_profiles_pkey PRIMARY KEY (id);


--
-- Name: user_profiles user_profiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_pkey PRIMARY KEY (id);


--
-- Name: user_profiles user_profiles_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_user_id_key UNIQUE (user_id);


--
-- Name: user_registration_data user_registration_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_registration_data
    ADD CONSTRAINT user_registration_data_pkey PRIMARY KEY (id);


--
-- Name: user_registration_data user_registration_data_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_registration_data
    ADD CONSTRAINT user_registration_data_user_id_key UNIQUE (user_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: value_propositions value_propositions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.value_propositions
    ADD CONSTRAINT value_propositions_pkey PRIMARY KEY (id);


--
-- Name: idx_activity_log_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_activity_log_created_at ON public.activity_log USING btree (created_at DESC);


--
-- Name: idx_activity_log_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_activity_log_user_id ON public.activity_log USING btree (user_id);


--
-- Name: idx_connections_contact_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_connections_contact_id ON public.connections USING btree (contact_id);


--
-- Name: idx_connections_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_connections_user_id ON public.connections USING btree (user_id);


--
-- Name: idx_contacts_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_contacts_email ON public.contacts USING btree (email);


--
-- Name: idx_contacts_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_contacts_user_id ON public.contacts USING btree (user_id);


--
-- Name: idx_cross_tier_approved; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cross_tier_approved ON public.cross_tier_requests USING btree (approved);


--
-- Name: idx_cross_tier_gatekeeper_passed; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cross_tier_gatekeeper_passed ON public.cross_tier_requests USING btree (gatekeeper_passed);


--
-- Name: idx_cross_tier_requester_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cross_tier_requester_id ON public.cross_tier_requests USING btree (requester_id);


--
-- Name: idx_cross_tier_target_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_cross_tier_target_id ON public.cross_tier_requests USING btree (target_id);


--
-- Name: idx_enhanced_matches_overall_score; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_enhanced_matches_overall_score ON public.enhanced_matches USING btree (overall_score DESC);


--
-- Name: idx_enhanced_matches_priority; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_enhanced_matches_priority ON public.enhanced_matches USING btree (priority);


--
-- Name: idx_enhanced_matches_seeker_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_enhanced_matches_seeker_id ON public.enhanced_matches USING btree (seeker_id);


--
-- Name: idx_enhanced_matches_seeker_needs; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_enhanced_matches_seeker_needs ON public.enhanced_matches USING gin (seeker_needs_addressed);


--
-- Name: idx_enhanced_matches_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_enhanced_matches_status ON public.enhanced_matches USING btree (status);


--
-- Name: idx_enhanced_matches_target_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_enhanced_matches_target_id ON public.enhanced_matches USING btree (target_id);


--
-- Name: idx_enhanced_matches_target_needs; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_enhanced_matches_target_needs ON public.enhanced_matches USING gin (target_needs_addressed);


--
-- Name: idx_enhanced_matches_tier_gap; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_enhanced_matches_tier_gap ON public.enhanced_matches USING btree (tier_gap);


--
-- Name: idx_introductions_introducer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_introductions_introducer_id ON public.introductions USING btree (introducer_id);


--
-- Name: idx_messages_recipient_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_messages_recipient_id ON public.messages USING btree (recipient_id);


--
-- Name: idx_messages_sender_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_messages_sender_id ON public.messages USING btree (sender_id);


--
-- Name: idx_messages_thread_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_messages_thread_id ON public.messages USING btree (thread_id);


--
-- Name: idx_network_snapshots_user_timestamp; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_network_snapshots_user_timestamp ON public.network_snapshots USING btree (user_id, "timestamp" DESC);


--
-- Name: idx_opportunities_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_opportunities_status ON public.opportunities USING btree (status);


--
-- Name: idx_opportunities_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_opportunities_user_id ON public.opportunities USING btree (user_id);


--
-- Name: idx_relationship_health_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_relationship_health_user_id ON public.relationship_health_history USING btree (user_id);


--
-- Name: idx_tier_profiles_contact_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tier_profiles_contact_id ON public.tier_profiles USING btree (contact_id);


--
-- Name: idx_tier_profiles_tier; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tier_profiles_tier ON public.tier_profiles USING btree (tier);


--
-- Name: idx_tier_profiles_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tier_profiles_user_id ON public.tier_profiles USING btree (user_id);


--
-- Name: idx_tier_profiles_verified; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tier_profiles_verified ON public.tier_profiles USING btree (verified);


--
-- Name: idx_user_profiles_expertise_areas; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_profiles_expertise_areas ON public.user_profiles USING gin (expertise_areas);


--
-- Name: idx_user_profiles_location; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_profiles_location ON public.user_profiles USING gin (location);


--
-- Name: idx_user_profiles_needs; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_profiles_needs ON public.user_profiles USING gin (needs);


--
-- Name: idx_user_profiles_offers; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_profiles_offers ON public.user_profiles USING gin (offers);


--
-- Name: idx_user_profiles_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_profiles_user_id ON public.user_profiles USING btree (user_id);


--
-- Name: idx_user_registration_can_offer; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_registration_can_offer ON public.user_registration_data USING gin (can_offer);


--
-- Name: idx_user_registration_created; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_registration_created ON public.user_registration_data USING btree (created_at);


--
-- Name: idx_user_registration_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_registration_email ON public.user_registration_data USING btree (email);


--
-- Name: idx_user_registration_industry; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_registration_industry ON public.user_registration_data USING btree (industry);


--
-- Name: idx_user_registration_location; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_registration_location ON public.user_registration_data USING btree (country, city);


--
-- Name: idx_user_registration_looking_for; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_registration_looking_for ON public.user_registration_data USING gin (looking_for);


--
-- Name: idx_user_registration_skills; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_registration_skills ON public.user_registration_data USING gin (technical_skills);


--
-- Name: idx_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_email ON public.users USING btree (email);


--
-- Name: idx_users_industry; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_industry ON public.users USING btree (industry);


--
-- Name: idx_value_props_category; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_value_props_category ON public.value_propositions USING btree (category);


--
-- Name: idx_value_props_proposer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_value_props_proposer_id ON public.value_propositions USING btree (proposer_id);


--
-- Name: idx_value_props_target_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_value_props_target_id ON public.value_propositions USING btree (target_id);


--
-- Name: idx_value_props_validated; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_value_props_validated ON public.value_propositions USING btree (validated);


--
-- Name: connections update_connections_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_connections_updated_at BEFORE UPDATE ON public.connections FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: enhanced_matches update_enhanced_matches_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_enhanced_matches_updated_at BEFORE UPDATE ON public.enhanced_matches FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: opportunities update_opportunities_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_opportunities_updated_at BEFORE UPDATE ON public.opportunities FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: tier_profiles update_tier_profiles_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_tier_profiles_updated_at BEFORE UPDATE ON public.tier_profiles FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: user_profiles update_user_profiles_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON public.user_profiles FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: users update_users_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: value_propositions update_value_propositions_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER update_value_propositions_updated_at BEFORE UPDATE ON public.value_propositions FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: user_registration_data user_registration_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER user_registration_updated_at BEFORE UPDATE ON public.user_registration_data FOR EACH ROW EXECUTE FUNCTION public.update_user_registration_updated_at();


--
-- Name: activity_log activity_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_log
    ADD CONSTRAINT activity_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: connections connections_contact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES public.contacts(id) ON DELETE CASCADE;


--
-- Name: connections connections_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.connections
    ADD CONSTRAINT connections_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: contacts contacts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: cross_tier_requests cross_tier_requests_requester_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cross_tier_requests
    ADD CONSTRAINT cross_tier_requests_requester_id_fkey FOREIGN KEY (requester_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: cross_tier_requests cross_tier_requests_target_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cross_tier_requests
    ADD CONSTRAINT cross_tier_requests_target_id_fkey FOREIGN KEY (target_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: cross_tier_requests cross_tier_requests_value_proposition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cross_tier_requests
    ADD CONSTRAINT cross_tier_requests_value_proposition_id_fkey FOREIGN KEY (value_proposition_id) REFERENCES public.value_propositions(id);


--
-- Name: enhanced_matches enhanced_matches_seeker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enhanced_matches
    ADD CONSTRAINT enhanced_matches_seeker_id_fkey FOREIGN KEY (seeker_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: enhanced_matches enhanced_matches_target_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enhanced_matches
    ADD CONSTRAINT enhanced_matches_target_id_fkey FOREIGN KEY (target_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: enhanced_matches enhanced_matches_value_proposition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.enhanced_matches
    ADD CONSTRAINT enhanced_matches_value_proposition_id_fkey FOREIGN KEY (value_proposition_id) REFERENCES public.value_propositions(id);


--
-- Name: introductions introductions_introducer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.introductions
    ADD CONSTRAINT introductions_introducer_id_fkey FOREIGN KEY (introducer_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: introductions introductions_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.introductions
    ADD CONSTRAINT introductions_message_id_fkey FOREIGN KEY (message_id) REFERENCES public.messages(id);


--
-- Name: introductions introductions_person1_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.introductions
    ADD CONSTRAINT introductions_person1_id_fkey FOREIGN KEY (person1_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: introductions introductions_person2_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.introductions
    ADD CONSTRAINT introductions_person2_id_fkey FOREIGN KEY (person2_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: messages messages_recipient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_recipient_id_fkey FOREIGN KEY (recipient_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: messages messages_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: network_snapshots network_snapshots_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.network_snapshots
    ADD CONSTRAINT network_snapshots_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: opportunities opportunities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.opportunities
    ADD CONSTRAINT opportunities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: relationship_health_history relationship_health_history_target_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relationship_health_history
    ADD CONSTRAINT relationship_health_history_target_user_id_fkey FOREIGN KEY (target_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: relationship_health_history relationship_health_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.relationship_health_history
    ADD CONSTRAINT relationship_health_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: tier_profiles tier_profiles_contact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tier_profiles
    ADD CONSTRAINT tier_profiles_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES public.contacts(id) ON DELETE CASCADE;


--
-- Name: tier_profiles tier_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tier_profiles
    ADD CONSTRAINT tier_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_profiles user_profiles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_profiles
    ADD CONSTRAINT user_profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_registration_data user_registration_data_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_registration_data
    ADD CONSTRAINT user_registration_data_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: value_propositions value_propositions_proposer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.value_propositions
    ADD CONSTRAINT value_propositions_proposer_id_fkey FOREIGN KEY (proposer_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: value_propositions value_propositions_target_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.value_propositions
    ADD CONSTRAINT value_propositions_target_id_fkey FOREIGN KEY (target_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO bondai_user;


--
-- Name: TABLE activity_log; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.activity_log TO bondai_user;


--
-- Name: TABLE user_profiles; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.user_profiles TO bondai_user;


--
-- Name: TABLE users; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.users TO bondai_user;


--
-- Name: TABLE connections; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.connections TO bondai_user;


--
-- Name: TABLE contacts; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.contacts TO bondai_user;


--
-- Name: TABLE cross_tier_requests; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.cross_tier_requests TO bondai_user;


--
-- Name: TABLE enhanced_matches; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.enhanced_matches TO bondai_user;


--
-- Name: TABLE introductions; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.introductions TO bondai_user;


--
-- Name: TABLE messages; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.messages TO bondai_user;


--
-- Name: TABLE network_snapshots; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.network_snapshots TO bondai_user;


--
-- Name: TABLE opportunities; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.opportunities TO bondai_user;


--
-- Name: TABLE relationship_health_history; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.relationship_health_history TO bondai_user;


--
-- Name: TABLE tier_profiles; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.tier_profiles TO bondai_user;


--
-- Name: TABLE value_propositions; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.value_propositions TO bondai_user;


--
-- PostgreSQL database dump complete
--

\unrestrict 5qfok7oogB6N8zmX8elOHaSIkoiQBj8G5e0b1DQrhg963HrQkpJa9d3XOMSabqv

