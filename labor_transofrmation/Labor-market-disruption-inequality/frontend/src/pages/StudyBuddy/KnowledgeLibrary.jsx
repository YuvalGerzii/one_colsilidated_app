/**
 * Knowledge Library Page
 * Browse and search learning resources from the Study Buddy platform
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Typography,
  Card,
  CardContent,
  CardMedia,
  CardActions,
  Button,
  Chip,
  TextField,
  InputAdornment,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Rating,
  Avatar,
  Stack,
  IconButton,
  Tooltip,
  Pagination,
  Skeleton,
  Drawer,
  Divider,
  Slider,
  FormControlLabel,
  Checkbox,
  Autocomplete,
  Paper,
  Badge,
} from '@mui/material';
import {
  Search,
  FilterList,
  Bookmark,
  BookmarkBorder,
  PlayCircle,
  Article,
  MenuBook,
  Code,
  Headphones,
  VideoLibrary,
  Star,
  Person,
  AccessTime,
  TrendingUp,
  Close,
  Sort,
  VerifiedUser,
  AttachMoney,
} from '@mui/icons-material';
import { studyBuddyAPI } from '../../services/api';

const RESOURCE_TYPES = {
  article: { icon: <Article />, label: 'Article', color: 'info' },
  video: { icon: <VideoLibrary />, label: 'Video', color: 'error' },
  course: { icon: <MenuBook />, label: 'Course', color: 'primary' },
  tutorial: { icon: <Code />, label: 'Tutorial', color: 'secondary' },
  podcast: { icon: <Headphones />, label: 'Podcast', color: 'success' },
  interactive: { icon: <PlayCircle />, label: 'Interactive', color: 'warning' },
};

const DIFFICULTY_LEVELS = ['beginner', 'intermediate', 'advanced', 'expert'];

const SORT_OPTIONS = [
  { value: 'relevance', label: 'Most Relevant' },
  { value: 'popularity', label: 'Most Popular' },
  { value: 'newest', label: 'Newest First' },
  { value: 'rating', label: 'Highest Rated' },
  { value: 'quality', label: 'Best Quality' },
  { value: 'duration', label: 'Duration' },
];

const POPULAR_TAGS = [
  'python', 'javascript', 'react', 'machine-learning', 'web-development',
  'data-science', 'devops', 'database', 'algorithms', 'cloud-computing',
  'ai', 'design-patterns', 'system-design', 'docker', 'kubernetes'
];

const KnowledgeLibrary = () => {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    query: '',
    resourceType: '',
    difficulty: '',
    tags: [],
    minQuality: 0,
    maxQuality: 100,
    minDuration: null,
    maxDuration: null,
    isFree: null,
    minPrice: null,
    maxPrice: null,
    verifiedOnly: false,
    minRating: 0,
  });
  const [sortBy, setSortBy] = useState('relevance');
  const [page, setPage] = useState(1);
  const [totalResults, setTotalResults] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [bookmarked, setBookmarked] = useState(new Set());
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const [facets, setFacets] = useState(null);

  useEffect(() => {
    loadResources();
  }, [filters, page, sortBy]);

  const loadResources = async () => {
    try {
      setLoading(true);

      // Build query parameters
      const params = new URLSearchParams();

      if (filters.query) params.append('query', filters.query);
      if (filters.resourceType) params.append('resource_type', filters.resourceType);
      if (filters.difficulty) params.append('difficulty', filters.difficulty);
      if (filters.tags && filters.tags.length > 0) {
        filters.tags.forEach(tag => params.append('tags', tag));
      }
      params.append('min_quality', filters.minQuality);
      params.append('max_quality', filters.maxQuality);
      if (filters.minDuration !== null) params.append('min_duration', filters.minDuration);
      if (filters.maxDuration !== null) params.append('max_duration', filters.maxDuration);
      if (filters.isFree !== null) params.append('is_free', filters.isFree);
      if (filters.minPrice !== null) params.append('min_price', filters.minPrice);
      if (filters.maxPrice !== null) params.append('max_price', filters.maxPrice);
      if (filters.verifiedOnly) params.append('verified_only', 'true');
      params.append('min_rating', filters.minRating);
      params.append('sort_by', sortBy);
      params.append('order', 'desc');
      params.append('limit', '12');
      params.append('offset', (page - 1) * 12);

      const response = await fetch(`/api/study-buddy/resources/search?${params.toString()}`);
      const data = await response.json();

      if (data.status === 'success') {
        setResources(data.results);
        setTotalResults(data.total_results);
        setTotalPages(Math.ceil(data.total_results / 12));
        setFacets(data.facets);
      }
    } catch (error) {
      console.error('Error loading resources:', error);
      // Fallback to empty results
      setResources([]);
      setTotalResults(0);
      setTotalPages(1);
    } finally {
      setLoading(false);
    }
  };

  const toggleBookmark = (resourceId) => {
    setBookmarked((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(resourceId)) {
        newSet.delete(resourceId);
      } else {
        newSet.add(resourceId);
      }
      return newSet;
    });
  };

  const getDifficultyColor = (level) => {
    const colors = {
      beginner: 'success',
      intermediate: 'info',
      advanced: 'warning',
      expert: 'error',
    };
    return colors[level] || 'default';
  };

  const clearAllFilters = () => {
    setFilters({
      query: '',
      resourceType: '',
      difficulty: '',
      tags: [],
      minQuality: 0,
      maxQuality: 100,
      minDuration: null,
      maxDuration: null,
      isFree: null,
      minPrice: null,
      maxPrice: null,
      verifiedOnly: false,
      minRating: 0,
    });
    setSortBy('relevance');
    setPage(1);
  };

  const getActiveFiltersCount = () => {
    let count = 0;
    if (filters.query) count++;
    if (filters.resourceType) count++;
    if (filters.difficulty) count++;
    if (filters.tags.length > 0) count++;
    if (filters.minQuality > 0 || filters.maxQuality < 100) count++;
    if (filters.minDuration !== null || filters.maxDuration !== null) count++;
    if (filters.isFree !== null) count++;
    if (filters.minPrice !== null || filters.maxPrice !== null) count++;
    if (filters.verifiedOnly) count++;
    if (filters.minRating > 0) count++;
    return count;
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Knowledge Library
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Discover high-quality learning resources from expert contributors
        </Typography>
      </Box>

      {/* Search and Filters */}
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={5}>
            <TextField
              fullWidth
              placeholder="Search resources by title, description, or tags..."
              value={filters.query}
              onChange={(e) => setFilters({ ...filters, query: e.target.value })}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>

          <Grid item xs={12} sm={6} md={2}>
            <FormControl fullWidth>
              <InputLabel>Type</InputLabel>
              <Select
                value={filters.resourceType}
                label="Type"
                onChange={(e) => setFilters({ ...filters, resourceType: e.target.value })}
              >
                <MenuItem value="">All Types</MenuItem>
                {Object.entries(RESOURCE_TYPES).map(([key, { label }]) => (
                  <MenuItem key={key} value={key}>
                    {label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6} md={2}>
            <FormControl fullWidth>
              <InputLabel>Difficulty</InputLabel>
              <Select
                value={filters.difficulty}
                label="Difficulty"
                onChange={(e) => setFilters({ ...filters, difficulty: e.target.value })}
              >
                <MenuItem value="">All Levels</MenuItem>
                {DIFFICULTY_LEVELS.map((level) => (
                  <MenuItem key={level} value={level}>
                    {level.charAt(0).toUpperCase() + level.slice(1)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6} md={2}>
            <FormControl fullWidth>
              <InputLabel>Sort By</InputLabel>
              <Select
                value={sortBy}
                label="Sort By"
                onChange={(e) => setSortBy(e.target.value)}
                startAdornment={
                  <InputAdornment position="start">
                    <Sort fontSize="small" />
                  </InputAdornment>
                }
              >
                {SORT_OPTIONS.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6} md={1}>
            <Badge badgeContent={getActiveFiltersCount()} color="primary">
              <Button
                variant="outlined"
                startIcon={<FilterList />}
                fullWidth
                onClick={() => setShowAdvancedFilters(true)}
                sx={{ height: 56 }}
              >
                Filters
              </Button>
            </Badge>
          </Grid>
        </Grid>

        {/* Active Filters Tags */}
        {getActiveFiltersCount() > 0 && (
          <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1, alignItems: 'center' }}>
            <Typography variant="caption" color="text.secondary">
              Active Filters:
            </Typography>
            {filters.tags.map((tag) => (
              <Chip
                key={tag}
                label={tag}
                size="small"
                onDelete={() => setFilters({ ...filters, tags: filters.tags.filter(t => t !== tag) })}
              />
            ))}
            {filters.verifiedOnly && (
              <Chip
                label="Verified Only"
                size="small"
                icon={<VerifiedUser />}
                onDelete={() => setFilters({ ...filters, verifiedOnly: false })}
              />
            )}
            {filters.isFree !== null && (
              <Chip
                label={filters.isFree ? "Free Only" : "Paid Only"}
                size="small"
                icon={<AttachMoney />}
                onDelete={() => setFilters({ ...filters, isFree: null })}
              />
            )}
            <Button size="small" onClick={clearAllFilters}>
              Clear All
            </Button>
          </Box>
        )}

        {/* Results Summary */}
        {!loading && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Found <strong>{totalResults}</strong> resources
              {filters.query && ` for "${filters.query}"`}
            </Typography>
          </Box>
        )}
      </Box>

      {/* Advanced Filters Drawer */}
      <Drawer
        anchor="right"
        open={showAdvancedFilters}
        onClose={() => setShowAdvancedFilters(false)}
      >
        <Box sx={{ width: 350, p: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h6" fontWeight={600}>
              Advanced Filters
            </Typography>
            <IconButton onClick={() => setShowAdvancedFilters(false)}>
              <Close />
            </IconButton>
          </Box>

          <Stack spacing={3}>
            {/* Tags Filter */}
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Tags
              </Typography>
              <Autocomplete
                multiple
                options={POPULAR_TAGS}
                value={filters.tags}
                onChange={(e, newValue) => setFilters({ ...filters, tags: newValue })}
                renderInput={(params) => (
                  <TextField {...params} placeholder="Select tags" size="small" />
                )}
                renderTags={(value, getTagProps) =>
                  value.map((option, index) => (
                    <Chip size="small" label={option} {...getTagProps({ index })} />
                  ))
                }
              />
            </Box>

            <Divider />

            {/* Quality Score Filter */}
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Quality Score: {filters.minQuality} - {filters.maxQuality}
              </Typography>
              <Slider
                value={[filters.minQuality, filters.maxQuality]}
                onChange={(e, newValue) => setFilters({ ...filters, minQuality: newValue[0], maxQuality: newValue[1] })}
                valueLabelDisplay="auto"
                min={0}
                max={100}
              />
            </Box>

            {/* Rating Filter */}
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Minimum Rating
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Rating
                  value={filters.minRating}
                  onChange={(e, newValue) => setFilters({ ...filters, minRating: newValue || 0 })}
                  precision={0.5}
                />
                <Typography variant="body2">
                  {filters.minRating > 0 ? `${filters.minRating}+` : 'Any'}
                </Typography>
              </Box>
            </Box>

            <Divider />

            {/* Duration Filter */}
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Duration (hours)
              </Typography>
              <Stack direction="row" spacing={1}>
                <TextField
                  label="Min"
                  type="number"
                  size="small"
                  value={filters.minDuration || ''}
                  onChange={(e) => setFilters({ ...filters, minDuration: e.target.value ? parseFloat(e.target.value) : null })}
                  fullWidth
                />
                <TextField
                  label="Max"
                  type="number"
                  size="small"
                  value={filters.maxDuration || ''}
                  onChange={(e) => setFilters({ ...filters, maxDuration: e.target.value ? parseFloat(e.target.value) : null })}
                  fullWidth
                />
              </Stack>
            </Box>

            <Divider />

            {/* Price Filter */}
            <Box>
              <Typography variant="subtitle2" gutterBottom>
                Price
              </Typography>
              <FormControl fullWidth size="small" sx={{ mb: 1 }}>
                <Select
                  value={filters.isFree === null ? 'all' : filters.isFree ? 'free' : 'paid'}
                  onChange={(e) => {
                    const value = e.target.value;
                    setFilters({
                      ...filters,
                      isFree: value === 'all' ? null : value === 'free'
                    });
                  }}
                >
                  <MenuItem value="all">All Resources</MenuItem>
                  <MenuItem value="free">Free Only</MenuItem>
                  <MenuItem value="paid">Paid Only</MenuItem>
                </Select>
              </FormControl>

              {filters.isFree === false && (
                <Stack direction="row" spacing={1} sx={{ mt: 1 }}>
                  <TextField
                    label="Min Credits"
                    type="number"
                    size="small"
                    value={filters.minPrice || ''}
                    onChange={(e) => setFilters({ ...filters, minPrice: e.target.value ? parseFloat(e.target.value) : null })}
                    fullWidth
                  />
                  <TextField
                    label="Max Credits"
                    type="number"
                    size="small"
                    value={filters.maxPrice || ''}
                    onChange={(e) => setFilters({ ...filters, maxPrice: e.target.value ? parseFloat(e.target.value) : null })}
                    fullWidth
                  />
                </Stack>
              )}
            </Box>

            <Divider />

            {/* Verified Only */}
            <FormControlLabel
              control={
                <Checkbox
                  checked={filters.verifiedOnly}
                  onChange={(e) => setFilters({ ...filters, verifiedOnly: e.target.checked })}
                />
              }
              label={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                  <VerifiedUser fontSize="small" color="primary" />
                  <Typography variant="body2">Verified Resources Only</Typography>
                </Box>
              }
            />

            {/* Action Buttons */}
            <Stack direction="row" spacing={2} sx={{ pt: 2 }}>
              <Button
                variant="outlined"
                fullWidth
                onClick={clearAllFilters}
              >
                Clear All
              </Button>
              <Button
                variant="contained"
                fullWidth
                onClick={() => setShowAdvancedFilters(false)}
              >
                Apply Filters
              </Button>
            </Stack>

            {/* Facets Display */}
            {facets && (
              <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.50', borderRadius: 1 }}>
                <Typography variant="caption" fontWeight={600} gutterBottom display="block">
                  Results Breakdown
                </Typography>
                <Typography variant="caption" color="text.secondary" display="block">
                  {facets.price_distribution?.free || 0} Free • {facets.price_distribution?.paid || 0} Paid
                </Typography>
              </Box>
            )}
          </Stack>
        </Box>
      </Drawer>

      {/* Resources Grid */}
      {loading ? (
        <Grid container spacing={3}>
          {[...Array(6)].map((_, index) => (
            <Grid item xs={12} sm={6} lg={4} key={index}>
              <Card>
                <Skeleton variant="rectangular" height={180} />
                <CardContent>
                  <Skeleton width="80%" height={32} />
                  <Skeleton width="100%" />
                  <Skeleton width="100%" />
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      ) : (
        <>
          <Grid container spacing={3}>
            {resources.map((resource) => {
              const resourceTypeInfo = RESOURCE_TYPES[resource.resource_type];

              return (
                <Grid item xs={12} sm={6} lg={4} key={resource.resource_id}>
                  <Card
                    sx={{
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      transition: 'transform 0.2s, box-shadow 0.2s',
                      '&:hover': {
                        transform: 'translateY(-4px)',
                        boxShadow: 6,
                      },
                    }}
                  >
                    {/* Thumbnail or Placeholder */}
                    <Box
                      sx={{
                        height: 180,
                        bgcolor: `${resourceTypeInfo.color}.50`,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        position: 'relative',
                      }}
                    >
                      <Box
                        sx={{
                          fontSize: 64,
                          color: `${resourceTypeInfo.color}.main`,
                          opacity: 0.3,
                        }}
                      >
                        {resourceTypeInfo.icon}
                      </Box>

                      {/* Quality Badge */}
                      <Chip
                        label={`${resource.quality_score}/100`}
                        size="small"
                        icon={<Star />}
                        sx={{
                          position: 'absolute',
                          top: 12,
                          right: 12,
                          fontWeight: 600,
                          bgcolor: 'white',
                        }}
                      />

                      {/* Bookmark */}
                      <IconButton
                        onClick={() => toggleBookmark(resource.resource_id)}
                        sx={{
                          position: 'absolute',
                          top: 8,
                          left: 8,
                          bgcolor: 'white',
                          '&:hover': { bgcolor: 'grey.100' },
                        }}
                      >
                        {bookmarked.has(resource.resource_id) ? (
                          <Bookmark color="primary" />
                        ) : (
                          <BookmarkBorder />
                        )}
                      </IconButton>
                    </Box>

                    <CardContent sx={{ flexGrow: 1 }}>
                      {/* Type and Difficulty */}
                      <Stack direction="row" spacing={1} sx={{ mb: 1.5 }}>
                        <Chip
                          icon={resourceTypeInfo.icon}
                          label={resourceTypeInfo.label}
                          size="small"
                          color={resourceTypeInfo.color}
                        />
                        <Chip
                          label={resource.difficulty_level}
                          size="small"
                          color={getDifficultyColor(resource.difficulty_level)}
                          variant="outlined"
                        />
                      </Stack>

                      {/* Title */}
                      <Typography variant="h6" fontWeight={600} gutterBottom>
                        {resource.title}
                      </Typography>

                      {/* Description */}
                      <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{
                          mb: 2,
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          display: '-webkit-box',
                          WebkitLineClamp: 2,
                          WebkitBoxOrient: 'vertical',
                        }}
                      >
                        {resource.description}
                      </Typography>

                      {/* Creator */}
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1.5 }}>
                        <Avatar sx={{ width: 24, height: 24, mr: 1, fontSize: '0.8rem' }}>
                          <Person />
                        </Avatar>
                        <Typography variant="caption" color="text.secondary">
                          {resource.creator_name}
                        </Typography>
                        <Chip
                          label={`${resource.creator_reputation}%`}
                          size="small"
                          sx={{ ml: 1, height: 20, fontSize: '0.7rem' }}
                        />
                      </Box>

                      {/* Stats */}
                      <Stack direction="row" spacing={2} sx={{ mb: 1.5 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <Rating value={resource.average_rating} size="small" readOnly precision={0.1} />
                          <Typography variant="caption" sx={{ ml: 0.5 }}>
                            ({resource.total_reviews})
                          </Typography>
                        </Box>
                      </Stack>

                      <Stack direction="row" spacing={2}>
                        <Tooltip title="Estimated time">
                          <Chip
                            icon={<AccessTime />}
                            label={`${resource.estimated_time_hours}h`}
                            size="small"
                            variant="outlined"
                          />
                        </Tooltip>
                        <Tooltip title="Views">
                          <Chip
                            icon={<TrendingUp />}
                            label={resource.views_count.toLocaleString()}
                            size="small"
                            variant="outlined"
                          />
                        </Tooltip>
                      </Stack>

                      {/* Tags */}
                      <Stack direction="row" spacing={0.5} sx={{ mt: 2, flexWrap: 'wrap', gap: 0.5 }}>
                        {resource.tags.slice(0, 3).map((tag) => (
                          <Chip key={tag} label={tag} size="small" variant="outlined" />
                        ))}
                      </Stack>
                    </CardContent>

                    <CardActions sx={{ p: 2, pt: 0 }}>
                      <Button
                        variant="contained"
                        fullWidth
                        disabled={!resource.is_free && resource.price_credits > 0}
                      >
                        {resource.is_free ? 'Start Learning' : `${resource.price_credits} Credits`}
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              );
            })}
          </Grid>

          {/* Pagination */}
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <Pagination
              count={totalPages}
              page={page}
              onChange={(e, value) => setPage(value)}
              color="primary"
              size="large"
            />
          </Box>
        </>
      )}
    </Box>
  );
};

export default KnowledgeLibrary;
