import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import {
  User,
  Briefcase,
  Target,
  Sparkles,
  ChevronRight,
  ChevronLeft,
  Check,
  MapPin,
  Globe,
  Code,
  Heart,
  TrendingUp,
  X,
  Lightbulb,
  Award,
  AlertCircle,
} from 'lucide-react';
import toast from 'react-hot-toast';

// Enhanced registration schema with contextual validation messages
const registrationSchema = z.object({
  // Step 1: Basic Info
  fullName: z.string().min(2, 'Please enter your full name (e.g., John Smith or Jane Doe)'),
  email: z.string().email('Please enter a valid email address (e.g., john@example.com)'),
  phone: z.string().optional(),
  country: z.string().min(1, 'Please select your country to help us find local matches'),
  city: z.string().min(1, 'Please enter your city (e.g., San Francisco, London, Tokyo)'),

  // Step 2: Professional Info
  jobTitle: z.string().min(2, 'Enter your job title (e.g., Software Engineer, Product Manager, Founder)'),
  company: z.string().min(1, 'Enter your company name or "Self-Employed" if applicable'),
  industry: z.string().min(1, 'Select your industry - this helps match you with relevant professionals'),
  yearsExperience: z.number().min(0, 'Years of experience must be 0 or greater').max(70, 'Please enter a valid number of years'),
  companySize: z.enum(['startup', 'small', 'medium', 'large', 'enterprise'], {
    errorMap: () => ({ message: 'Please select your company size' })
  }),

  // Step 3: Skills & Expertise
  technicalSkills: z.array(z.object({
    skill: z.string().min(1, 'Skill name is required'),
    level: z.enum(['beginner', 'intermediate', 'advanced', 'expert']),
    years: z.number().optional(),
  })).min(1, 'Add at least one technical skill (e.g., JavaScript, Python, Product Management)'),

  softSkills: z.array(z.string()).min(1, 'Select at least one soft skill - this helps us understand your working style'),
  domainExpertise: z.array(z.string()).min(1, 'Add at least one area of expertise (e.g., Web Development, Marketing, Finance)'),

  // Step 4: Goals & Preferences
  lookingFor: z.array(z.string()).min(1, 'Select what you\'re looking for - you can select multiple options'),
  lookingForDetails: z.string().optional(),
  canOffer: z.array(z.string()).min(1, 'Select what you can offer - this helps create value exchange'),
  canOfferDetails: z.string().optional(),
  professionalGoals: z.string().min(10, 'Describe your goals in at least 10 characters (e.g., "Launch my SaaS product and reach 1000 users")'),
  timeCommitment: z.enum(['few-hours', 'part-time', 'full-time', 'flexible'], {
    errorMap: () => ({ message: 'Please select your available time commitment' })
  }),

  // Step 5: Matching Preferences (for algorithm)
  urgency: z.enum(['immediate', 'high', 'medium', 'low'], {
    errorMap: () => ({ message: 'Please indicate how urgent your need is' })
  }),
  timeline: z.enum(['1-week', '1-month', '3-months', '6-months', 'ongoing'], {
    errorMap: () => ({ message: 'Please select your expected timeline' })
  }),
  relationshipType: z.enum(['one-time', 'short-term', 'long-term', 'ongoing'], {
    errorMap: () => ({ message: 'Please select the type of relationship you\'re seeking' })
  }),
  communicationStyle: z.array(z.string()).min(1, 'Select at least one communication preference - this ensures compatibility'),
  workingStyle: z.array(z.string()).min(1, 'Select at least one working style - helps match you with compatible professionals'),
  geographicPreference: z.enum(['local-only', 'regional', 'national', 'global', 'remote-first'], {
    errorMap: () => ({ message: 'Please indicate your geographic preference' })
  }),
  preferredIndustries: z.array(z.string()).optional(),
  budgetRange: z.string().optional(),
  dealBreakers: z.string().optional(),
  successCriteria: z.string().min(10, 'Describe success criteria (e.g., "Product launched with 100 users and $10K MRR")'),
  pastCollaborationExperience: z.string().optional(),
  specificChallenges: z.string().optional(),

  // Optional fields
  bio: z.string().optional(),
  linkedinUrl: z.string().url('Please enter a valid URL (e.g., https://linkedin.com/in/yourname)').optional().or(z.literal('')),
  portfolioUrl: z.string().url('Please enter a valid URL (e.g., https://yourportfolio.com)').optional().or(z.literal('')),
});

type RegistrationFormData = z.infer<typeof registrationSchema>;

interface EnhancedRegistrationProps {
  onComplete: (data: RegistrationFormData) => Promise<void>;
  initialData?: Partial<RegistrationFormData>;
}

const INDUSTRIES = [
  'Technology', 'Software/SaaS', 'FinTech', 'Finance', 'Banking', 'Investment',
  'Healthcare', 'Biotech', 'Pharmaceuticals', 'Medical Devices',
  'Education', 'EdTech', 'E-learning',
  'E-commerce', 'Retail', 'Consumer Goods',
  'Marketing', 'Advertising', 'Public Relations',
  'Consulting', 'Professional Services',
  'Manufacturing', 'Automotive', 'Aerospace',
  'Real Estate', 'Construction', 'Architecture',
  'Legal', 'Law Firm',
  'Media & Entertainment', 'Gaming', 'Music', 'Film/TV',
  'Telecommunications', 'Networking',
  'Energy', 'Renewable Energy', 'Oil & Gas',
  'Transportation', 'Logistics', 'Supply Chain',
  'Hospitality', 'Tourism', 'Food & Beverage',
  'Agriculture', 'Farming',
  'Non-profit', 'Social Impact', 'Government',
  'Sports', 'Fitness', 'Wellness',
  'Fashion', 'Beauty', 'Cosmetics',
  'Insurance', 'Risk Management',
  'Cybersecurity', 'Data & Analytics',
  'Blockchain', 'Cryptocurrency',
  'Artificial Intelligence', 'Robotics', 'IoT',
  'Other',
];

const POPULAR_SKILLS = [
  // Programming Languages
  'JavaScript', 'Python', 'TypeScript', 'Java', 'C++', 'C#', 'Go', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Rust',

  // Web Development
  'React', 'Angular', 'Vue.js', 'Node.js', 'Express', 'Next.js', 'HTML/CSS', 'GraphQL', 'REST APIs',

  // Mobile Development
  'iOS Development', 'Android Development', 'React Native', 'Flutter', 'Mobile UI/UX',

  // Cloud & DevOps
  'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'CI/CD', 'Terraform', 'Jenkins',

  // Data & AI
  'Machine Learning', 'Deep Learning', 'Data Science', 'Data Analysis', 'SQL', 'NoSQL', 'Big Data', 'TensorFlow', 'PyTorch',

  // Design
  'UI/UX Design', 'Figma', 'Adobe XD', 'Sketch', 'Graphic Design', 'Web Design', 'Product Design',

  // Business & Management
  'Product Management', 'Project Management', 'Business Strategy', 'Agile/Scrum', 'Team Leadership',

  // Marketing & Sales
  'Digital Marketing', 'Content Marketing', 'SEO/SEM', 'Social Media Marketing', 'Sales', 'Business Development',

  // Finance & Legal
  'Financial Analysis', 'Accounting', 'Investment Banking', 'Legal', 'Compliance', 'Contract Negotiation',

  // Industry Specific
  'FinTech', 'HealthTech', 'EdTech', 'E-commerce', 'Blockchain', 'Cybersecurity', 'IoT',
];

const SOFT_SKILLS = [
  'Leadership', 'Communication', 'Team Collaboration', 'Problem Solving',
  'Critical Thinking', 'Creativity', 'Adaptability', 'Time Management',
  'Negotiation', 'Mentoring', 'Public Speaking', 'Emotional Intelligence',
];

const LOOKING_FOR_OPTIONS = [
  'Mentorship', 'Co-founder', 'Business Partner', 'Investor',
  'Technical Advisor', 'Marketing Help', 'Sales Support', 'Industry Connections',
  'Career Advice', 'Collaboration Opportunities',
];

const CAN_OFFER_OPTIONS = [
  'Mentorship', 'Technical Expertise', 'Business Advice', 'Industry Connections',
  'Funding/Investment', 'Marketing Support', 'Design Help', 'Product Feedback',
  'Introductions', 'Office Hours',
];

const COMMUNICATION_STYLES = [
  'Email', 'Video Calls', 'Phone Calls', 'In-Person Meetings',
  'Slack/Chat', 'Asynchronous', 'Regular Check-ins', 'Ad-hoc as needed',
];

const WORKING_STYLES = [
  'Highly Structured', 'Flexible/Adaptive', 'Collaborative', 'Independent',
  'Data-Driven', 'Intuitive', 'Fast-Paced', 'Methodical',
  'Hands-On', 'Strategic', 'Detail-Oriented', 'Big Picture',
];

const BUDGET_RANGES = [
  'Free/Barter', 'Under $1K', '$1K-$5K', '$5K-$10K',
  '$10K-$50K', '$50K-$100K', '$100K+', 'Equity-based', 'Revenue Share',
];

// Smart skill suggestions based on job title
const ROLE_SKILL_SUGGESTIONS: Record<string, string[]> = {
  'software engineer': ['JavaScript', 'Python', 'React', 'Node.js', 'SQL', 'Git'],
  'frontend developer': ['React', 'TypeScript', 'HTML/CSS', 'JavaScript', 'Vue.js', 'Next.js'],
  'backend developer': ['Python', 'Node.js', 'SQL', 'REST APIs', 'Docker', 'AWS'],
  'full stack developer': ['JavaScript', 'React', 'Node.js', 'SQL', 'TypeScript', 'AWS'],
  'data scientist': ['Python', 'Machine Learning', 'SQL', 'Data Analysis', 'TensorFlow', 'PyTorch'],
  'product manager': ['Product Management', 'Agile/Scrum', 'Data Analysis', 'Leadership', 'Business Strategy'],
  'ui/ux designer': ['Figma', 'UI/UX Design', 'Adobe XD', 'Product Design', 'Web Design'],
  'marketing manager': ['Digital Marketing', 'SEO/SEM', 'Content Marketing', 'Social Media Marketing', 'Data Analysis'],
  'devops engineer': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Terraform', 'Jenkins'],
  'mobile developer': ['React Native', 'iOS Development', 'Android Development', 'Flutter', 'Mobile UI/UX'],
};

// Calculate profile strength
const calculateProfileStrength = (data: Partial<RegistrationFormData>): {
  percentage: number;
  level: string;
  color: string;
  suggestions: string[];
} => {
  let score = 0;
  const suggestions: string[] = [];

  // Basic info (20 points)
  if (data.fullName && data.email) score += 10;
  if (data.country && data.city) score += 10;

  // Professional info (20 points)
  if (data.jobTitle && data.company) score += 10;
  if (data.industry && data.yearsExperience !== undefined) score += 10;

  // Skills (25 points)
  if (data.technicalSkills && data.technicalSkills.length >= 3) {
    score += 15;
  } else if (data.technicalSkills && data.technicalSkills.length > 0) {
    score += 8;
    suggestions.push('Add more technical skills for better matches');
  } else {
    suggestions.push('Add your technical skills');
  }

  if (data.softSkills && data.softSkills.length >= 3) {
    score += 10;
  } else {
    suggestions.push('Select at least 3 soft skills');
  }

  // Goals & offerings (20 points)
  if (data.lookingFor && data.lookingFor.length > 0) score += 10;
  if (data.canOffer && data.canOffer.length > 0) score += 10;

  // Detailed preferences (15 points)
  if (data.lookingForDetails && data.lookingForDetails.length > 20) score += 5;
  if (data.canOfferDetails && data.canOfferDetails.length > 20) score += 5;
  if (data.professionalGoals && data.professionalGoals.length > 50) score += 5;

  // Matching preferences (15 points)  if (data.urgency && data.timeline) score += 5;
  if (data.communicationStyle && data.communicationStyle.length > 0) score += 5;
  if (data.successCriteria && data.successCriteria.length > 20) score += 5;

  // Optional but valuable (5 points)
  if (data.bio && data.bio.length > 30) score += 2;
  if (data.linkedinUrl) score += 2;
  if (data.portfolioUrl) score += 1;

  let level = 'Incomplete';
  let color = 'red';

  if (score >= 90) {
    level = 'Excellent';
    color = 'green';
  } else if (score >= 75) {
    level = 'Great';
    color = 'blue';
  } else if (score >= 60) {
    level = 'Good';
    color = 'yellow';
  } else if (score >= 40) {
    level = 'Fair';
    color = 'orange';
  }

  // Add strategic suggestions
  if (!data.successCriteria) {
    suggestions.push('Define your success criteria for better matching');
  }
  if (!data.communicationStyle || data.communicationStyle.length === 0) {
    suggestions.push('Select communication preferences to find compatible matches');
  }
  if (!data.specificChallenges) {
    suggestions.push('Describe your challenges to help us find relevant experts');
  }

  return {
    percentage: score,
    level,
    color,
    suggestions: suggestions.slice(0, 3), // Top 3 suggestions
  };
};

// Get smart skill suggestions
const getSkillSuggestions = (jobTitle: string): string[] => {
  const titleLower = jobTitle.toLowerCase();

  for (const [role, skills] of Object.entries(ROLE_SKILL_SUGGESTIONS)) {
    if (titleLower.includes(role)) {
      return skills;
    }
  }

  // Default suggestions
  return ['Leadership', 'Communication', 'Problem Solving'];
};

// Get character count status for text fields
const getCharacterCountStatus = (
  currentLength: number,
  config: {
    min?: number;
    recommended?: number;
    max?: number;
    fieldName: string;
  }
): {
  color: string;
  message: string;
  showCount: boolean;
} => {
  const { min, recommended, max, fieldName } = config;

  // If there's a minimum and we haven't met it
  if (min && currentLength < min) {
    return {
      color: 'text-red-600',
      message: `${currentLength}/${min} characters (minimum required)`,
      showCount: true,
    };
  }

  // If there's a recommended length and we haven't met it
  if (recommended && currentLength < recommended) {
    return {
      color: 'text-yellow-600',
      message: `${currentLength}/${recommended} characters (recommended for better matches)`,
      showCount: true,
    };
  }

  // If we've met the recommended length or minimum
  if ((recommended && currentLength >= recommended) || (min && currentLength >= min)) {
    return {
      color: 'text-green-600',
      message: `${currentLength} characters - Great! Detailed information helps our AI find better matches.`,
      showCount: true,
    };
  }

  // For optional fields with no content
  if (currentLength === 0) {
    return {
      color: 'text-gray-500',
      message: 'Optional - Add details for better matching',
      showCount: false,
    };
  }

  // For optional fields with some content
  if (currentLength > 0 && currentLength < 30) {
    return {
      color: 'text-blue-600',
      message: `${currentLength} characters - Add more details for better matches`,
      showCount: true,
    };
  }

  // For optional fields with good content
  return {
    color: 'text-green-600',
    message: `${currentLength} characters - Excellent! This helps our matching algorithm.`,
    showCount: true,
  };
};

export default function EnhancedRegistration({ onComplete, initialData }: EnhancedRegistrationProps) {
  const [currentStep, setCurrentStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [skillSuggestions, setSkillSuggestions] = useState<string[]>([]);
  const [showSkillSuggestions, setShowSkillSuggestions] = useState(false);
  const [profileStrength, setProfileStrength] = useState({ percentage: 0, level: 'Incomplete', color: 'red', suggestions: [] as string[] });
  const totalSteps = 5;

  const {
    register,
    handleSubmit,
    control,
    watch,
    setValue,
    trigger,
    formState: { errors },
  } = useForm<RegistrationFormData>({
    resolver: zodResolver(registrationSchema),
    defaultValues: initialData || {
      technicalSkills: [],
      softSkills: [],
      domainExpertise: [],
      lookingFor: [],
      lookingForDetails: '',
      canOffer: [],
      canOfferDetails: '',
      communicationStyle: [],
      workingStyle: [],
      preferredIndustries: [],
    },
  });

  const formData = watch();
  const technicalSkills = watch('technicalSkills') || [];
  const softSkills = watch('softSkills') || [];
  const domainExpertise = watch('domainExpertise') || [];
  const lookingFor = watch('lookingFor') || [];
  const canOffer = watch('canOffer') || [];
  const communicationStyle = watch('communicationStyle') || [];
  const workingStyle = watch('workingStyle') || [];
  const preferredIndustries = watch('preferredIndustries') || [];
  const jobTitle = watch('jobTitle') || '';

  // Watch text fields for character counting
  const lookingForDetails = watch('lookingForDetails') || '';
  const canOfferDetails = watch('canOfferDetails') || '';
  const professionalGoals = watch('professionalGoals') || '';
  const successCriteria = watch('successCriteria') || '';
  const dealBreakers = watch('dealBreakers') || '';
  const specificChallenges = watch('specificChallenges') || '';
  const pastCollaborationExperience = watch('pastCollaborationExperience') || '';
  const bio = watch('bio') || '';

  // Calculate profile strength in real-time
  useEffect(() => {
    const strength = calculateProfileStrength(formData);
    setProfileStrength(strength);
  }, [formData]);

  // Generate skill suggestions based on job title
  useEffect(() => {
    if (jobTitle && jobTitle.length > 3) {
      const suggestions = getSkillSuggestions(jobTitle);
      setSkillSuggestions(suggestions);
      setShowSkillSuggestions(true);
    } else {
      setShowSkillSuggestions(false);
    }
  }, [jobTitle]);

  const addTechnicalSkill = () => {
    setValue('technicalSkills', [...technicalSkills, { skill: '', level: 'intermediate' as const }]);
  };

  const removeTechnicalSkill = (index: number) => {
    setValue('technicalSkills', technicalSkills.filter((_, i) => i !== index));
  };

  const addSkillFromSuggestion = (skill: string) => {
    const exists = technicalSkills.some(s => s.skill === skill);
    if (!exists) {
      setValue('technicalSkills', [...technicalSkills, { skill, level: 'intermediate' as const }]);
      toast.success(`Added ${skill} to your skills`);
    }
  };

  const toggleArrayItem = (array: string[], item: string, setter: (items: string[]) => void) => {
    if (array.includes(item)) {
      setter(array.filter(i => i !== item));
    } else {
      setter([...array, item]);
    }
  };

  const nextStep = async () => {
    const fieldsToValidate = getFieldsForStep(currentStep);
    const isValid = await trigger(fieldsToValidate as any);

    if (isValid) {
      setCurrentStep(currentStep + 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const prevStep = () => {
    setCurrentStep(currentStep - 1);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const getFieldsForStep = (step: number): (keyof RegistrationFormData)[] => {
    switch (step) {
      case 1:
        return ['fullName', 'email', 'country', 'city'];
      case 2:
        return ['jobTitle', 'company', 'industry', 'yearsExperience', 'companySize'];
      case 3:
        return ['technicalSkills', 'softSkills', 'domainExpertise'];
      case 4:
        return ['lookingFor', 'canOffer', 'professionalGoals', 'timeCommitment'];
      case 5:
        return ['urgency', 'timeline', 'relationshipType', 'communicationStyle', 'workingStyle', 'geographicPreference', 'successCriteria'];
      default:
        return [];
    }
  };

  const onSubmit = async (data: RegistrationFormData) => {
    setIsSubmitting(true);
    try {
      await onComplete(data);
      toast.success('Registration completed successfully!');
    } catch (error: any) {
      toast.error(error.message || 'Failed to complete registration');
    } finally {
      setIsSubmitting(false);
    }
  };

  const progressPercentage = (currentStep / totalSteps) * 100;

  // Get contextual tips based on user's goals
  const getContextualTips = () => {
    const tips: string[] = [];

    if (lookingFor.includes('Funding/Investment')) {
      tips.push('💡 For fundraising: Mention your traction, stage, and amount seeking in details');
    }
    if (lookingFor.includes('Co-Founder')) {
      tips.push('💡 For co-founder search: Be specific about complementary skills you need');
    }
    if (lookingFor.includes('Mentorship')) {
      tips.push('💡 For mentorship: Clearly articulate what you want to learn');
    }
    if (lookingFor.includes('Technical Advisor')) {
      tips.push('💡 For advisors: Describe the specific technical challenges you face');
    }
    if (canOffer.includes('Funding/Investment')) {
      tips.push('💰 As an investor: Specify your check size and preferred stages');
    }
    if (canOffer.includes('Mentorship')) {
      tips.push('🎓 As a mentor: Share your areas of expertise and availability');
    }

    return tips;
  };

  const contextualTips = getContextualTips();

  // Estimate match quality
  const getMatchQualityEstimate = () => {
    const completionScore = profileStrength.percentage;
    const hasSpecificNeeds = lookingFor.length > 0;
    const hasSpecificOfferings = canOffer.length > 0;
    const hasDetailedGoals = (formData.professionalGoals?.length || 0) > 50;
    const hasPreferences = (communicationStyle.length > 0) || (workingStyle.length > 0);

    let estimatedMatches = 0;
    let quality = 'Low';
    let color = 'red';

    if (completionScore >= 75 && hasSpecificNeeds && hasDetailedGoals) {
      estimatedMatches = Math.floor(15 + (completionScore - 75) * 0.6); // 15-30 matches
      quality = 'Excellent';
      color = 'green';
    } else if (completionScore >= 60 && hasSpecificNeeds) {
      estimatedMatches = Math.floor(8 + (completionScore - 60) * 0.47); // 8-15 matches
      quality = 'Good';
      color = 'blue';
    } else if (completionScore >= 40 && hasSpecificNeeds) {
      estimatedMatches = Math.floor(3 + (completionScore - 40) * 0.25); // 3-8 matches
      quality = 'Fair';
      color = 'yellow';
    } else if (hasSpecificNeeds || hasSpecificOfferings) {
      estimatedMatches = Math.floor(1 + completionScore * 0.05); // 1-5 matches
      quality = 'Limited';
      color = 'orange';
    }

    return {
      estimatedMatches,
      quality,
      color,
      message: estimatedMatches > 15 ? 'Your profile is attracting high-quality matches!' :
               estimatedMatches > 8 ? 'Good profile! Add more details for better matches.' :
               estimatedMatches > 3 ? 'Complete your profile to unlock more matches.' :
               'Add more information to start getting matched.'
    };
  };

  const matchEstimate = getMatchQualityEstimate();

  // Get preview of next step
  const getNextStepPreview = (step: number): { title: string; description: string; highlights: string[] } | null => {
    switch (step) {
      case 1:
        return {
          title: 'Next: Professional Profile',
          description: 'Tell us about your work experience',
          highlights: ['Job title and company', 'Industry and experience level', 'Company size']
        };
      case 2:
        return {
          title: 'Next: Skills & Expertise',
          description: 'Showcase your technical and soft skills',
          highlights: ['Technical skills with proficiency levels', 'Soft skills selection', 'Domain expertise areas']
        };
      case 3:
        return {
          title: 'Next: Goals & Preferences',
          description: 'Define what you\'re looking for and what you can offer',
          highlights: ['What you need help with', 'What you can provide', 'Professional goals and time commitment']
        };
      case 4:
        return {
          title: 'Next: Matching Preferences',
          description: 'Help our AI find your perfect matches',
          highlights: ['Communication and working style', 'Geographic preferences', 'Success criteria and deal breakers']
        };
      default:
        return null;
    }
  };

  const nextStepPreview = getNextStepPreview(currentStep);

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <div>
              <span className="text-sm font-medium text-gray-700">
                Step {currentStep} of {totalSteps}
              </span>
              <span className="text-xs text-gray-500 ml-2">
                • Total time: ~20 minutes
              </span>
            </div>
            <span className="text-sm font-medium text-primary-600">
              {Math.round(progressPercentage)}% Complete
            </span>
          </div>
          <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-primary-600 to-secondary-600"
              initial={{ width: 0 }}
              animate={{ width: `${progressPercentage}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>

        {/* Profile Strength Indicator */}
        {profileStrength.percentage > 0 && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`mb-6 bg-white rounded-xl shadow-lg border-2 ${
              profileStrength.color === 'green' ? 'border-green-500' :
              profileStrength.color === 'blue' ? 'border-blue-500' :
              profileStrength.color === 'yellow' ? 'border-yellow-500' :
              profileStrength.color === 'orange' ? 'border-orange-500' :
              'border-red-500'
            } p-4`}
          >
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-2">
                <Award className={`w-5 h-5 ${
                  profileStrength.color === 'green' ? 'text-green-600' :
                  profileStrength.color === 'blue' ? 'text-blue-600' :
                  profileStrength.color === 'yellow' ? 'text-yellow-600' :
                  profileStrength.color === 'orange' ? 'text-orange-600' :
                  'text-red-600'
                }`} />
                <span className="font-semibold text-gray-900">Profile Strength: {profileStrength.level}</span>
              </div>
              <span className={`text-lg font-bold ${
                profileStrength.color === 'green' ? 'text-green-600' :
                profileStrength.color === 'blue' ? 'text-blue-600' :
                profileStrength.color === 'yellow' ? 'text-yellow-600' :
                profileStrength.color === 'orange' ? 'text-orange-600' :
                'text-red-600'
              }`}>
                {profileStrength.percentage}%
              </span>
            </div>
            <div className="h-2 bg-gray-200 rounded-full overflow-hidden mb-3">
              <motion.div
                className={`h-full ${
                  profileStrength.color === 'green' ? 'bg-green-500' :
                  profileStrength.color === 'blue' ? 'bg-blue-500' :
                  profileStrength.color === 'yellow' ? 'bg-yellow-500' :
                  profileStrength.color === 'orange' ? 'bg-orange-500' :
                  'bg-red-500'
                }`}
                initial={{ width: 0 }}
                animate={{ width: `${profileStrength.percentage}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
            {profileStrength.suggestions.length > 0 && (
              <div className="space-y-1">
                {profileStrength.suggestions.map((suggestion, idx) => (
                  <div key={idx} className="flex items-start space-x-2 text-sm text-gray-600">
                    <Lightbulb className="w-4 h-4 text-yellow-500 mt-0.5 flex-shrink-0" />
                    <span>{suggestion}</span>
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        )}

        {/* Match Quality Estimate */}
        {matchEstimate.estimatedMatches > 0 && currentStep >= 3 && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className={`mb-6 bg-white rounded-xl shadow-lg border-2 ${
              matchEstimate.color === 'green' ? 'border-green-400' :
              matchEstimate.color === 'blue' ? 'border-blue-400' :
              matchEstimate.color === 'yellow' ? 'border-yellow-400' :
              'border-orange-400'
            } p-4`}
          >
            <div className="flex items-center justify-between">
              <div>
                <div className="flex items-center space-x-2 mb-1">
                  <TrendingUp className={`w-5 h-5 ${
                    matchEstimate.color === 'green' ? 'text-green-600' :
                    matchEstimate.color === 'blue' ? 'text-blue-600' :
                    matchEstimate.color === 'yellow' ? 'text-yellow-600' :
                    'text-orange-600'
                  }`} />
                  <span className="font-semibold text-gray-900">Estimated Matches</span>
                </div>
                <p className="text-sm text-gray-600">{matchEstimate.message}</p>
              </div>
              <div className="text-right">
                <div className={`text-3xl font-bold ${
                  matchEstimate.color === 'green' ? 'text-green-600' :
                  matchEstimate.color === 'blue' ? 'text-blue-600' :
                  matchEstimate.color === 'yellow' ? 'text-yellow-600' :
                  'text-orange-600'
                }`}>
                  {matchEstimate.estimatedMatches}+
                </div>
                <div className="text-xs text-gray-500 uppercase tracking-wide">
                  {matchEstimate.quality} Quality
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* Form Card */}
        <motion.div
          className="bg-white rounded-2xl shadow-xl p-8"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <form onSubmit={handleSubmit(onSubmit)}>
            <AnimatePresence mode="wait">
              {/* Step 1: Basic Information */}
              {currentStep === 1 && (
                <motion.div
                  key="step1"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-6"
                >
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 rounded-xl bg-primary-100 flex items-center justify-center">
                        <User className="w-6 h-6 text-primary-600" />
                      </div>
                      <div>
                        <h2 className="text-2xl font-bold text-gray-900">Basic Information</h2>
                        <p className="text-gray-600">Let's start with the essentials</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">
                        ~2 min
                      </span>
                    </div>
                  </div>

                  <div>
                    <label className="label">Full Name *</label>
                    <input
                      {...register('fullName')}
                      className="input"
                      placeholder="John Doe"
                    />
                    {errors.fullName && (
                      <p className="text-sm text-red-600 mt-1">{errors.fullName.message}</p>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="label">Email *</label>
                      <input
                        {...register('email')}
                        type="email"
                        className="input"
                        placeholder="john@example.com"
                      />
                      {errors.email && (
                        <p className="text-sm text-red-600 mt-1">{errors.email.message}</p>
                      )}
                    </div>

                    <div>
                      <label className="label">Phone</label>
                      <input
                        {...register('phone')}
                        className="input"
                        placeholder="+1 (555) 123-4567"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="label">Country *</label>
                      <div className="relative">
                        <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <input
                          {...register('country')}
                          className="input pl-11"
                          placeholder="United States"
                        />
                      </div>
                      {errors.country && (
                        <p className="text-sm text-red-600 mt-1">{errors.country.message}</p>
                      )}
                    </div>

                    <div>
                      <label className="label">City *</label>
                      <input
                        {...register('city')}
                        className="input"
                        placeholder="San Francisco"
                      />
                      {errors.city && (
                        <p className="text-sm text-red-600 mt-1">{errors.city.message}</p>
                      )}
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Step 2: Professional Information */}
              {currentStep === 2 && (
                <motion.div
                  key="step2"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-6"
                >
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 rounded-xl bg-secondary-100 flex items-center justify-center">
                        <Briefcase className="w-6 h-6 text-secondary-600" />
                      </div>
                      <div>
                        <h2 className="text-2xl font-bold text-gray-900">Professional Profile</h2>
                        <p className="text-gray-600">Tell us about your professional background</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">
                        ~3 min
                      </span>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="label">Job Title *</label>
                      <input
                        {...register('jobTitle')}
                        className="input"
                        placeholder="Software Engineer"
                      />
                      {errors.jobTitle && (
                        <p className="text-sm text-red-600 mt-1">{errors.jobTitle.message}</p>
                      )}
                    </div>

                    <div>
                      <label className="label">Company *</label>
                      <input
                        {...register('company')}
                        className="input"
                        placeholder="Tech Corp"
                      />
                      {errors.company && (
                        <p className="text-sm text-red-600 mt-1">{errors.company.message}</p>
                      )}
                    </div>
                  </div>

                  <div>
                    <label className="label">Industry *</label>
                    <select {...register('industry')} className="input">
                      <option value="">Select an industry</option>
                      {INDUSTRIES.map((industry) => (
                        <option key={industry} value={industry.toLowerCase()}>
                          {industry}
                        </option>
                      ))}
                    </select>
                    {errors.industry && (
                      <p className="text-sm text-red-600 mt-1">{errors.industry.message}</p>
                    )}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="label">Years of Experience *</label>
                      <input
                        {...register('yearsExperience', { valueAsNumber: true })}
                        type="number"
                        min="0"
                        max="70"
                        className="input"
                        placeholder="5"
                      />
                      {errors.yearsExperience && (
                        <p className="text-sm text-red-600 mt-1">{errors.yearsExperience.message}</p>
                      )}
                    </div>

                    <div>
                      <label className="label">Company Size *</label>
                      <select {...register('companySize')} className="input">
                        <option value="">Select size</option>
                        <option value="startup">Startup (1-10)</option>
                        <option value="small">Small (11-50)</option>
                        <option value="medium">Medium (51-200)</option>
                        <option value="large">Large (201-1000)</option>
                        <option value="enterprise">Enterprise (1000+)</option>
                      </select>
                      {errors.companySize && (
                        <p className="text-sm text-red-600 mt-1">{errors.companySize.message}</p>
                      )}
                    </div>
                  </div>
                </motion.div>
              )}

              {/* Step 3: Skills & Expertise */}
              {currentStep === 3 && (
                <motion.div
                  key="step3"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-6"
                >
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 rounded-xl bg-accent-100 flex items-center justify-center">
                        <Code className="w-6 h-6 text-accent-600" />
                      </div>
                      <div>
                        <h2 className="text-2xl font-bold text-gray-900">Skills & Expertise</h2>
                        <p className="text-gray-600">Showcase your capabilities</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">
                        ~5 min
                      </span>
                    </div>
                  </div>

                  {/* Technical Skills */}
                  <div>
                    <label className="label">Technical Skills *</label>
                    <div className="space-y-3 mb-3">
                      {technicalSkills.map((skill, index) => (
                        <div key={index} className="flex gap-3">
                          <input
                            {...register(`technicalSkills.${index}.skill` as const)}
                            className="input flex-1"
                            placeholder="e.g., Python, React, AWS"
                            list="skill-suggestions"
                          />
                          <select
                            {...register(`technicalSkills.${index}.level` as const)}
                            className="input w-40"
                          >
                            <option value="beginner">Beginner</option>
                            <option value="intermediate">Intermediate</option>
                            <option value="advanced">Advanced</option>
                            <option value="expert">Expert</option>
                          </select>
                          <button
                            type="button"
                            onClick={() => removeTechnicalSkill(index)}
                            className="btn-ghost p-2"
                          >
                            <X className="w-5 h-5" />
                          </button>
                        </div>
                      ))}
                    </div>
                    <datalist id="skill-suggestions">
                      {POPULAR_SKILLS.map((skill) => (
                        <option key={skill} value={skill} />
                      ))}
                    </datalist>
                    <button
                      type="button"
                      onClick={addTechnicalSkill}
                      className="btn-outline"
                    >
                      + Add Skill
                    </button>
                    {errors.technicalSkills && (
                      <p className="text-sm text-red-600 mt-1">{errors.technicalSkills.message}</p>
                    )}

                    {/* Smart Skill Suggestions */}
                    {showSkillSuggestions && skillSuggestions.length > 0 && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg"
                      >
                        <div className="flex items-center space-x-2 mb-3">
                          <Sparkles className="w-5 h-5 text-blue-600" />
                          <span className="font-medium text-blue-900">Suggested skills for {jobTitle}</span>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {skillSuggestions.map((skill) => {
                            const alreadyAdded = technicalSkills.some(s => s.skill === skill);
                            return (
                              <button
                                key={skill}
                                type="button"
                                onClick={() => addSkillFromSuggestion(skill)}
                                disabled={alreadyAdded}
                                className={`px-3 py-1 rounded-full text-sm font-medium transition-all ${
                                  alreadyAdded
                                    ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                                    : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                                }`}
                              >
                                {alreadyAdded ? `✓ ${skill}` : `+ ${skill}`}
                              </button>
                            );
                          })}
                        </div>
                      </motion.div>
                    )}
                  </div>

                  {/* Soft Skills */}
                  <div>
                    <label className="label">Soft Skills *</label>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mb-2">
                      {SOFT_SKILLS.map((skill) => (
                        <button
                          key={skill}
                          type="button"
                          onClick={() => toggleArrayItem(softSkills, skill, (items) => setValue('softSkills', items))}
                          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                            softSkills.includes(skill)
                              ? 'bg-primary-600 text-white'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {skill}
                        </button>
                      ))}
                    </div>
                    {errors.softSkills && (
                      <p className="text-sm text-red-600 mt-1">{errors.softSkills.message}</p>
                    )}
                  </div>

                  {/* Domain Expertise */}
                  <div>
                    <label className="label">Domain Expertise *</label>
                    <p className="text-sm text-gray-600 mb-2">What areas do you specialize in?</p>
                    <div className="flex flex-wrap gap-2">
                      {domainExpertise.map((domain, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center gap-1 px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm"
                        >
                          {domain}
                          <button
                            type="button"
                            onClick={() => setValue('domainExpertise', domainExpertise.filter((_, i) => i !== index))}
                            className="hover:text-primary-900"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </span>
                      ))}
                    </div>
                    <input
                      className="input mt-2"
                      placeholder="Type and press Enter"
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                          e.preventDefault();
                          const input = e.currentTarget;
                          if (input.value.trim()) {
                            setValue('domainExpertise', [...domainExpertise, input.value.trim()]);
                            input.value = '';
                          }
                        }
                      }}
                    />
                    {errors.domainExpertise && (
                      <p className="text-sm text-red-600 mt-1">{errors.domainExpertise.message}</p>
                    )}
                  </div>
                </motion.div>
              )}

              {/* Step 4: Goals & Preferences */}
              {currentStep === 4 && (
                <motion.div
                  key="step4"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-6"
                >
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 rounded-xl bg-green-100 flex items-center justify-center">
                        <Target className="w-6 h-6 text-green-600" />
                      </div>
                      <div>
                        <h2 className="text-2xl font-bold text-gray-900">Goals & Preferences</h2>
                        <p className="text-gray-600">Help us find your perfect match</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">
                        ~4 min
                      </span>
                    </div>
                  </div>

                  {/* Looking For */}
                  <div>
                    <label className="label">What are you looking for? *</label>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mb-3">
                      {LOOKING_FOR_OPTIONS.map((option) => (
                        <button
                          key={option}
                          type="button"
                          onClick={() => toggleArrayItem(lookingFor, option, (items) => setValue('lookingFor', items))}
                          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                            lookingFor.includes(option)
                              ? 'bg-secondary-600 text-white'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {option}
                        </button>
                      ))}
                    </div>
                    {errors.lookingFor && (
                      <p className="text-sm text-red-600 mt-1">{errors.lookingFor.message}</p>
                    )}

                    <div className="mt-3">
                      <label className="label text-sm text-gray-600">Additional details (optional)</label>
                      <textarea
                        {...register('lookingForDetails')}
                        className="input min-h-[80px]"
                        placeholder="Provide any additional details about what you're looking for..."
                      />
                      {(() => {
                        const status = getCharacterCountStatus(lookingForDetails.length, {
                          recommended: 50,
                          fieldName: 'lookingForDetails'
                        });
                        return (
                          <p className={`text-xs mt-1 ${status.color}`}>
                            {status.message}
                          </p>
                        );
                      })()}
                    </div>
                  </div>

                  {/* Can Offer */}
                  <div>
                    <label className="label">What can you offer? *</label>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mb-3">
                      {CAN_OFFER_OPTIONS.map((option) => (
                        <button
                          key={option}
                          type="button"
                          onClick={() => toggleArrayItem(canOffer, option, (items) => setValue('canOffer', items))}
                          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                            canOffer.includes(option)
                              ? 'bg-accent-600 text-white'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {option}
                        </button>
                      ))}
                    </div>
                    {errors.canOffer && (
                      <p className="text-sm text-red-600 mt-1">{errors.canOffer.message}</p>
                    )}

                    <div className="mt-3">
                      <label className="label text-sm text-gray-600">Additional details (optional)</label>
                      <textarea
                        {...register('canOfferDetails')}
                        className="input min-h-[80px]"
                        placeholder="Provide any additional details about what you can offer..."
                      />
                      {(() => {
                        const status = getCharacterCountStatus(canOfferDetails.length, {
                          recommended: 50,
                          fieldName: 'canOfferDetails'
                        });
                        return (
                          <p className={`text-xs mt-1 ${status.color}`}>
                            {status.message}
                          </p>
                        );
                      })()}
                    </div>
                  </div>

                  {/* Contextual Tips */}
                  {contextualTips.length > 0 && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="p-4 bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg"
                    >
                      <div className="flex items-start space-x-2 mb-2">
                        <AlertCircle className="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" />
                        <span className="font-medium text-purple-900">Pro Tips for Your Selection</span>
                      </div>
                      <div className="space-y-1 ml-7">
                        {contextualTips.map((tip, idx) => (
                          <p key={idx} className="text-sm text-gray-700">{tip}</p>
                        ))}
                      </div>
                    </motion.div>
                  )}

                  {/* Professional Goals */}
                  <div>
                    <label className="label">Professional Goals *</label>
                    <textarea
                      {...register('professionalGoals')}
                      className="input min-h-[120px]"
                      placeholder="Describe your short-term and long-term professional goals..."
                    />
                    {errors.professionalGoals && (
                      <p className="text-sm text-red-600 mt-1">{errors.professionalGoals.message}</p>
                    )}
                    {(() => {
                      const status = getCharacterCountStatus(professionalGoals.length, {
                        min: 10,
                        recommended: 100,
                        fieldName: 'professionalGoals'
                      });
                      return (
                        <p className={`text-xs mt-1 ${status.color}`}>
                          {status.message}
                        </p>
                      );
                    })()}
                  </div>

                  {/* Time Commitment */}
                  <div>
                    <label className="label">Time Commitment *</label>
                    <select {...register('timeCommitment')} className="input">
                      <option value="">Select your availability</option>
                      <option value="few-hours">A few hours per month</option>
                      <option value="part-time">Part-time (10-20 hours/week)</option>
                      <option value="full-time">Full-time commitment</option>
                      <option value="flexible">Flexible</option>
                    </select>
                    {errors.timeCommitment && (
                      <p className="text-sm text-red-600 mt-1">{errors.timeCommitment.message}</p>
                    )}
                  </div>
                </motion.div>
              )}

              {/* Step 5: Matching Preferences */}
              {currentStep === 5 && (
                <motion.div
                  key="step5"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-6"
                >
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center space-x-3">
                      <div className="w-12 h-12 rounded-xl bg-purple-100 flex items-center justify-center">
                        <Sparkles className="w-6 h-6 text-purple-600" />
                      </div>
                      <div>
                        <h2 className="text-2xl font-bold text-gray-900">Matching Preferences</h2>
                        <p className="text-gray-600">Help our AI find your perfect matches</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">
                        ~6 min
                      </span>
                    </div>
                  </div>

                  {/* Urgency & Timeline */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="label">Urgency *</label>
                      <p className="text-xs text-gray-500 mb-2">How urgent is your need?</p>
                      <select {...register('urgency')} className="input">
                        <option value="">Select urgency level</option>
                        <option value="immediate">Immediate (ASAP)</option>
                        <option value="high">High (Within 1-2 weeks)</option>
                        <option value="medium">Medium (Within 1-2 months)</option>
                        <option value="low">Low (Flexible timing)</option>
                      </select>
                      {errors.urgency && (
                        <p className="text-sm text-red-600 mt-1">{errors.urgency.message}</p>
                      )}
                    </div>

                    <div>
                      <label className="label">Timeline *</label>
                      <p className="text-xs text-gray-500 mb-2">Expected duration of engagement</p>
                      <select {...register('timeline')} className="input">
                        <option value="">Select timeline</option>
                        <option value="1-week">1 Week</option>
                        <option value="1-month">1 Month</option>
                        <option value="3-months">3 Months</option>
                        <option value="6-months">6 Months</option>
                        <option value="ongoing">Ongoing/Long-term</option>
                      </select>
                      {errors.timeline && (
                        <p className="text-sm text-red-600 mt-1">{errors.timeline.message}</p>
                      )}
                    </div>
                  </div>

                  {/* Relationship Type */}
                  <div>
                    <label className="label">Relationship Type *</label>
                    <p className="text-xs text-gray-500 mb-2">What type of relationship are you seeking?</p>
                    <select {...register('relationshipType')} className="input">
                      <option value="">Select relationship type</option>
                      <option value="one-time">One-time engagement</option>
                      <option value="short-term">Short-term collaboration</option>
                      <option value="long-term">Long-term partnership</option>
                      <option value="ongoing">Ongoing relationship</option>
                    </select>
                    {errors.relationshipType && (
                      <p className="text-sm text-red-600 mt-1">{errors.relationshipType.message}</p>
                    )}
                  </div>

                  {/* Communication Style */}
                  <div>
                    <label className="label">Communication Preferences *</label>
                    <p className="text-xs text-gray-500 mb-2">How do you prefer to communicate?</p>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                      {COMMUNICATION_STYLES.map((style) => (
                        <button
                          key={style}
                          type="button"
                          onClick={() => toggleArrayItem(communicationStyle, style, (items) => setValue('communicationStyle', items))}
                          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                            communicationStyle.includes(style)
                              ? 'bg-purple-600 text-white'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {style}
                        </button>
                      ))}
                    </div>
                    {errors.communicationStyle && (
                      <p className="text-sm text-red-600 mt-1">{errors.communicationStyle.message}</p>
                    )}
                  </div>

                  {/* Working Style */}
                  <div>
                    <label className="label">Working Style *</label>
                    <p className="text-xs text-gray-500 mb-2">Select all that describe your working style</p>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                      {WORKING_STYLES.map((style) => (
                        <button
                          key={style}
                          type="button"
                          onClick={() => toggleArrayItem(workingStyle, style, (items) => setValue('workingStyle', items))}
                          className={`px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                            workingStyle.includes(style)
                              ? 'bg-blue-600 text-white'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {style}
                        </button>
                      ))}
                    </div>
                    {errors.workingStyle && (
                      <p className="text-sm text-red-600 mt-1">{errors.workingStyle.message}</p>
                    )}
                  </div>

                  {/* Geographic Preference */}
                  <div>
                    <label className="label">Geographic Preference *</label>
                    <p className="text-xs text-gray-500 mb-2">Where are you open to connecting?</p>
                    <select {...register('geographicPreference')} className="input">
                      <option value="">Select geographic preference</option>
                      <option value="local-only">Local only (same city)</option>
                      <option value="regional">Regional (same state/province)</option>
                      <option value="national">National (same country)</option>
                      <option value="global">Global (anywhere)</option>
                      <option value="remote-first">Remote-first (location doesn't matter)</option>
                    </select>
                    {errors.geographicPreference && (
                      <p className="text-sm text-red-600 mt-1">{errors.geographicPreference.message}</p>
                    )}
                  </div>

                  {/* Preferred Industries */}
                  <div>
                    <label className="label">Preferred Industries (Optional)</label>
                    <p className="text-xs text-gray-500 mb-2">Select specific industries you want to connect with</p>
                    <div className="max-h-40 overflow-y-auto border rounded-lg p-3 bg-gray-50">
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                        {INDUSTRIES.map((industry) => (
                          <label key={industry} className="flex items-center space-x-2 text-sm">
                            <input
                              type="checkbox"
                              checked={preferredIndustries.includes(industry)}
                              onChange={(e) => {
                                if (e.target.checked) {
                                  setValue('preferredIndustries', [...preferredIndustries, industry]);
                                } else {
                                  setValue('preferredIndustries', preferredIndustries.filter(i => i !== industry));
                                }
                              }}
                              className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                            />
                            <span>{industry}</span>
                          </label>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Budget Range */}
                  <div>
                    <label className="label">Budget Range (Optional)</label>
                    <p className="text-xs text-gray-500 mb-2">What's your budget or what are you willing to invest?</p>
                    <select {...register('budgetRange')} className="input">
                      <option value="">Select budget range</option>
                      {BUDGET_RANGES.map((range) => (
                        <option key={range} value={range}>{range}</option>
                      ))}
                    </select>
                  </div>

                  {/* Success Criteria */}
                  <div>
                    <label className="label">Success Criteria *</label>
                    <p className="text-xs text-gray-500 mb-2">What does success look like for this connection?</p>
                    <textarea
                      {...register('successCriteria')}
                      className="input min-h-[100px]"
                      placeholder="E.g., Successfully launch our product, secure funding, hire 3 developers, grow revenue by 30%..."
                    />
                    {errors.successCriteria && (
                      <p className="text-sm text-red-600 mt-1">{errors.successCriteria.message}</p>
                    )}
                    {(() => {
                      const status = getCharacterCountStatus(successCriteria.length, {
                        min: 10,
                        recommended: 80,
                        fieldName: 'successCriteria'
                      });
                      return (
                        <p className={`text-xs mt-1 ${status.color}`}>
                          {status.message}
                        </p>
                      );
                    })()}
                  </div>

                  {/* Deal Breakers */}
                  <div>
                    <label className="label">Deal Breakers (Optional)</label>
                    <p className="text-xs text-gray-500 mb-2">Are there any absolute requirements or things you won't compromise on?</p>
                    <textarea
                      {...register('dealBreakers')}
                      className="input min-h-[80px]"
                      placeholder="E.g., Must have experience in fintech, must be available for weekly calls, must be in the same timezone..."
                    />
                    {(() => {
                      const status = getCharacterCountStatus(dealBreakers.length, {
                        recommended: 40,
                        fieldName: 'dealBreakers'
                      });
                      return (
                        <p className={`text-xs mt-1 ${status.color}`}>
                          {status.message}
                        </p>
                      );
                    })()}
                  </div>

                  {/* Specific Challenges */}
                  <div>
                    <label className="label">Specific Challenges (Optional)</label>
                    <p className="text-xs text-gray-500 mb-2">What specific problems are you trying to solve?</p>
                    <textarea
                      {...register('specificChallenges')}
                      className="input min-h-[80px]"
                      placeholder="E.g., Struggling with user acquisition, need help with technical architecture, looking for advice on fundraising strategy..."
                    />
                    {(() => {
                      const status = getCharacterCountStatus(specificChallenges.length, {
                        recommended: 50,
                        fieldName: 'specificChallenges'
                      });
                      return (
                        <p className={`text-xs mt-1 ${status.color}`}>
                          {status.message}
                        </p>
                      );
                    })()}
                  </div>

                  {/* Past Collaboration Experience */}
                  <div>
                    <label className="label">Past Collaboration Experience (Optional)</label>
                    <p className="text-xs text-gray-500 mb-2">Have you had similar collaborations before? What worked or didn't work?</p>
                    <textarea
                      {...register('pastCollaborationExperience')}
                      className="input min-h-[80px]"
                      placeholder="E.g., Worked with a mentor before but struggled with time zones, had great success with async communication..."
                    />
                    {(() => {
                      const status = getCharacterCountStatus(pastCollaborationExperience.length, {
                        recommended: 50,
                        fieldName: 'pastCollaborationExperience'
                      });
                      return (
                        <p className={`text-xs mt-1 ${status.color}`}>
                          {status.message}
                        </p>
                      );
                    })()}
                  </div>

                  {/* Optional Fields */}
                  <div className="border-t pt-6">
                    <h3 className="text-lg font-semibold mb-4">Optional Information</h3>

                    <div className="space-y-4">
                      <div>
                        <label className="label">Bio</label>
                        <textarea
                          {...register('bio')}
                          className="input min-h-[80px]"
                          placeholder="Tell us more about yourself..."
                        />
                        {(() => {
                          const status = getCharacterCountStatus(bio.length, {
                            recommended: 60,
                            fieldName: 'bio'
                          });
                          return (
                            <p className={`text-xs mt-1 ${status.color}`}>
                              {status.message}
                            </p>
                          );
                        })()}
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="label">LinkedIn URL</label>
                          <div className="relative">
                            <Globe className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <input
                              {...register('linkedinUrl')}
                              className="input pl-11"
                              placeholder="https://linkedin.com/in/..."
                            />
                          </div>
                        </div>

                        <div>
                          <label className="label">Portfolio URL</label>
                          <div className="relative">
                            <Globe className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                            <input
                              {...register('portfolioUrl')}
                              className="input pl-11"
                              placeholder="https://yourportfolio.com"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Next Step Preview */}
            {nextStepPreview && currentStep < totalSteps && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg"
              >
                <div className="flex items-start space-x-3">
                  <ChevronRight className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                  <div className="flex-1">
                    <h4 className="font-semibold text-blue-900 mb-1">{nextStepPreview.title}</h4>
                    <p className="text-sm text-blue-700 mb-2">{nextStepPreview.description}</p>
                    <ul className="space-y-1">
                      {nextStepPreview.highlights.map((highlight, idx) => (
                        <li key={idx} className="text-xs text-blue-600 flex items-center">
                          <span className="w-1 h-1 bg-blue-400 rounded-full mr-2"></span>
                          {highlight}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Navigation Buttons */}
            <div className="flex items-center justify-between mt-8 pt-6 border-t">
              <button
                type="button"
                onClick={prevStep}
                disabled={currentStep === 1}
                className="btn-ghost disabled:opacity-0 disabled:cursor-not-allowed"
              >
                <ChevronLeft className="w-5 h-5 mr-2" />
                Previous
              </button>

              {currentStep < totalSteps ? (
                <button
                  type="button"
                  onClick={nextStep}
                  className="btn-primary"
                >
                  Next
                  <ChevronRight className="w-5 h-5 ml-2" />
                </button>
              ) : (
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="btn-primary"
                >
                  {isSubmitting ? (
                    <>
                      <span className="animate-spin mr-2">⏳</span>
                      Submitting...
                    </>
                  ) : (
                    <>
                      <Check className="w-5 h-5 mr-2" />
                      Complete Registration
                    </>
                  )}
                </button>
              )}
            </div>
          </form>
        </motion.div>

        {/* Step Indicators */}
        <div className="flex justify-center mt-8 space-x-2">
          {Array.from({ length: totalSteps }).map((_, index) => (
            <div
              key={index}
              className={`h-2 w-2 rounded-full transition-all ${
                index + 1 === currentStep
                  ? 'w-8 bg-primary-600'
                  : index + 1 < currentStep
                  ? 'bg-primary-600'
                  : 'bg-gray-300'
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
