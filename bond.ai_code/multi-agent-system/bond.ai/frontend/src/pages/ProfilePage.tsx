import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import {
  User,
  ArrowLeft,
  Mail,
  MapPin,
  Briefcase,
  Link as LinkIcon,
  Edit,
  Target,
  Gift,
  ExternalLink,
} from 'lucide-react';
import { useAuthStore } from '../store/authStore';
import { profileApi } from '../lib/api';
import { getPriorityColor } from '../lib/utils';

export default function ProfilePage() {
  const { user } = useAuthStore();

  const { data: profile, isLoading } = useQuery({
    queryKey: ['profile', user?.id],
    queryFn: () => profileApi.getProfile(user!.id),
    enabled: !!user,
  });

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200">
        <div className="container-custom">
          <div className="flex items-center justify-between h-16">
            <Link to="/dashboard" className="flex items-center space-x-2">
              <ArrowLeft className="w-5 h-5 text-gray-600" />
              <span className="text-gray-900 font-medium">Back to Dashboard</span>
            </Link>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container-custom py-8 max-w-4xl">
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin w-12 h-12 border-4 border-primary-600 border-t-transparent rounded-full mx-auto" />
            <p className="text-gray-600 mt-4">Loading profile...</p>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Profile Header */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="card"
            >
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-start space-x-4">
                  <div className="w-20 h-20 rounded-full bg-gradient-primary flex items-center justify-center">
                    <User className="w-10 h-10 text-white" />
                  </div>
                  <div>
                    <h1 className="text-2xl font-bold text-gray-900">{user?.name}</h1>
                    <div className="flex items-center space-x-2 text-gray-600 mt-1">
                      <Mail className="w-4 h-4" />
                      <span>{user?.email}</span>
                    </div>
                  </div>
                </div>
                <Link to="/profile/edit" className="btn-outline">
                  <Edit className="w-4 h-4 mr-2" />
                  Edit Profile
                </Link>
              </div>

              {profile && (
                <>
                  {profile.bio && (
                    <p className="text-gray-700 mb-4">{profile.bio}</p>
                  )}

                  <div className="grid md:grid-cols-2 gap-4">
                    {profile.industry && (
                      <div className="flex items-center space-x-2 text-gray-600">
                        <Briefcase className="w-4 h-4" />
                        <span>{profile.industry}</span>
                      </div>
                    )}
                    {profile.location && (
                      <div className="flex items-center space-x-2 text-gray-600">
                        <MapPin className="w-4 h-4" />
                        <span>{profile.location}</span>
                      </div>
                    )}
                  </div>

                  {(profile.linkedinUrl || profile.websiteUrl) && (
                    <div className="flex flex-wrap gap-3 mt-4 pt-4 border-t border-gray-200">
                      {profile.linkedinUrl && (
                        <a
                          href={profile.linkedinUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center text-sm text-primary-600 hover:text-primary-700"
                        >
                          <LinkIcon className="w-4 h-4 mr-1" />
                          LinkedIn
                          <ExternalLink className="w-3 h-3 ml-1" />
                        </a>
                      )}
                      {profile.websiteUrl && (
                        <a
                          href={profile.websiteUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center text-sm text-primary-600 hover:text-primary-700"
                        >
                          <LinkIcon className="w-4 h-4 mr-1" />
                          Website
                          <ExternalLink className="w-3 h-3 ml-1" />
                        </a>
                      )}
                    </div>
                  )}
                </>
              )}
            </motion.div>

            {/* Needs */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="card"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <Target className="w-5 h-5 text-blue-600" />
                  <h2 className="text-xl font-bold text-gray-900">What I Need</h2>
                </div>
                <span className="text-sm text-gray-600">
                  {profile?.needs?.length || 0} needs
                </span>
              </div>

              {profile?.needs && profile.needs.length > 0 ? (
                <div className="space-y-3">
                  {profile.needs.map((need) => (
                    <div key={need.id} className="border border-blue-200 bg-blue-50 rounded-lg p-4">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-semibold text-blue-900">{need.category}</h3>
                        <span
                          className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(
                            need.priority
                          )}`}
                        >
                          {need.priority}
                        </span>
                      </div>
                      <p className="text-sm text-blue-700">{need.description}</p>
                      {need.tags && need.tags.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-2">
                          {need.tags.map((tag, i) => (
                            <span
                              key={i}
                              className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs"
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-600 text-center py-8">
                  No needs added yet. Edit your profile to add what you're looking for.
                </p>
              )}
            </motion.div>

            {/* Offerings */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="card"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <Gift className="w-5 h-5 text-green-600" />
                  <h2 className="text-xl font-bold text-gray-900">What I Offer</h2>
                </div>
                <span className="text-sm text-gray-600">
                  {profile?.offerings?.length || 0} offerings
                </span>
              </div>

              {profile?.offerings && profile.offerings.length > 0 ? (
                <div className="space-y-3">
                  {profile.offerings.map((offering) => (
                    <div
                      key={offering.id}
                      className="border border-green-200 bg-green-50 rounded-lg p-4"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-semibold text-green-900">{offering.category}</h3>
                        <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">
                          {offering.capacity}
                        </span>
                      </div>
                      <p className="text-sm text-green-700">{offering.description}</p>
                      {offering.tags && offering.tags.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-2">
                          {offering.tags.map((tag, i) => (
                            <span
                              key={i}
                              className="px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs"
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-600 text-center py-8">
                  No offerings added yet. Edit your profile to add what you can provide.
                </p>
              )}
            </motion.div>
          </div>
        )}
      </div>
    </div>
  );
}
