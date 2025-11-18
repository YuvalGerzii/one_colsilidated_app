import React, { useMemo, useState } from 'react';
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Box,
  Button,
  Card,
  CardActionArea,
  CardContent,
  Divider,
  Grid,
  IconButton,
  Stack,
  Tooltip,
  Typography,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  UploadFile as UploadFileIcon,
  Delete as DeleteIcon,
  ArrowForward as ArrowForwardIcon,
  PictureAsPdf as PictureAsPdfIcon,
  InsertDriveFile as InsertDriveFileIcon,
  CloudDownload as CloudDownloadIcon,
  Folder as FolderIcon,
} from '@mui/icons-material';

interface LibraryFile {
  id: string;
  name: string;
  type: 'pdf' | 'image' | 'excel' | 'word';
  updatedAt: string;
  owner: string;
  folder: string;
}

const FILE_PREVIEWS: Record<LibraryFile['type'], JSX.Element> = {
  pdf: <PictureAsPdfIcon color="error" sx={{ fontSize: 36 }} />,
  image: <InsertDriveFileIcon color="secondary" sx={{ fontSize: 36 }} />,
  excel: <InsertDriveFileIcon color="success" sx={{ fontSize: 36 }} />,
  word: <InsertDriveFileIcon color="primary" sx={{ fontSize: 36 }} />,
};

const FOLDERS = [
  {
    name: 'Investment Committee',
    children: ['Decks', 'Approval Letters', 'IC Notes'],
  },
  {
    name: 'Due Diligence',
    children: ['Financials', 'Legal', 'Operational'],
  },
  {
    name: 'Reporting',
    children: ['LP Reports', 'Audit'],
  },
];

const mockFiles: LibraryFile[] = [
  {
    id: '1',
    name: 'Q1 Board Update.pdf',
    type: 'pdf',
    updatedAt: 'Apr 12, 2024',
    owner: 'Alex Morgan',
    folder: 'Reporting',
  },
  {
    id: '2',
    name: 'Lender Model.xlsx',
    type: 'excel',
    updatedAt: 'Mar 08, 2024',
    owner: 'Priya Patel',
    folder: 'Due Diligence',
  },
  {
    id: '3',
    name: 'Site Visit Photos.zip',
    type: 'image',
    updatedAt: 'Jan 29, 2024',
    owner: 'Chris Howard',
    folder: 'Due Diligence',
  },
  {
    id: '4',
    name: 'SPA Draft.docx',
    type: 'word',
    updatedAt: 'Feb 21, 2024',
    owner: 'Jamie Chen',
    folder: 'Investment Committee',
  },
];

export const DocumentsLibrary: React.FC = () => {
  const [selectedFolder, setSelectedFolder] = useState<string>('All documents');
  const filteredFiles = useMemo(
    () =>
      selectedFolder === 'All documents'
        ? mockFiles
        : mockFiles.filter((file) => file.folder === selectedFolder),
    [selectedFolder]
  );

  return (
    <Box>
      <Stack direction={{ xs: 'column', md: 'row' }} justifyContent="space-between" mb={4} spacing={3}>
        <Box>
          <Typography variant="h4" gutterBottom>
            Documents Library
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Browse structured folders, preview files, and move deliverables into organized workspaces.
          </Typography>
        </Box>
        <Stack direction="row" spacing={2}>
          <Button variant="outlined" startIcon={<FolderIcon />}>New folder</Button>
          <Button variant="contained" startIcon={<UploadFileIcon />}>Upload</Button>
        </Stack>
      </Stack>

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Box sx={{ position: 'sticky', top: 96 }}>
            <Typography variant="subtitle2" color="text.secondary" gutterBottom>
              Folder tree
            </Typography>
            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Typography>All documents</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <Stack spacing={1}>
                  <Button
                    variant={selectedFolder === 'All documents' ? 'contained' : 'text'}
                    color={selectedFolder === 'All documents' ? 'primary' : 'inherit'}
                    size="small"
                    onClick={() => setSelectedFolder('All documents')}
                    sx={{ justifyContent: 'flex-start' }}
                  >
                    All documents
                  </Button>
                  {FOLDERS.map((folder) => (
                    <Box key={folder.name}>
                      <Button
                        variant={selectedFolder === folder.name ? 'contained' : 'text'}
                        color={selectedFolder === folder.name ? 'primary' : 'inherit'}
                        size="small"
                        onClick={() => setSelectedFolder(folder.name)}
                        sx={{ justifyContent: 'flex-start' }}
                      >
                        {folder.name}
                      </Button>
                      <Stack pl={2} spacing={0.5} mt={1}>
                        {folder.children.map((child) => (
                          <Button key={child} size="small" sx={{ justifyContent: 'flex-start' }}>
                            {child}
                          </Button>
                        ))}
                      </Stack>
                    </Box>
                  ))}
                </Stack>
              </AccordionDetails>
            </Accordion>
          </Box>
        </Grid>

        <Grid item xs={12} md={6}>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            Files in {selectedFolder}
          </Typography>
          <Grid container spacing={2}>
            {filteredFiles.map((file) => (
              <Grid item xs={12} sm={6} key={file.id}>
                <Card>
                  <CardActionArea>
                    <CardContent>
                      <Stack direction="row" spacing={2} alignItems="center" mb={2}>
                        {FILE_PREVIEWS[file.type]}
                        <Box>
                          <Typography variant="subtitle1">{file.name}</Typography>
                          <Typography variant="body2" color="text.secondary">
                            Updated {file.updatedAt}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Owner: {file.owner}
                          </Typography>
                        </Box>
                      </Stack>
                      <Divider sx={{ my: 2 }} />
                      <Stack direction="row" justifyContent="space-between" alignItems="center">
                        <Typography variant="caption" color="text.secondary">
                          Stored in {file.folder}
                        </Typography>
                        <Stack direction="row" spacing={1}>
                          <Tooltip title="Download">
                            <IconButton size="small">
                              <CloudDownloadIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Move">
                            <IconButton size="small">
                              <ArrowForwardIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Delete">
                            <IconButton size="small">
                              <DeleteIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        </Stack>
                      </Stack>
                    </CardContent>
                  </CardActionArea>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>

        <Grid item xs={12} md={3}>
          <Card sx={{ position: { md: 'sticky' }, top: { md: 96 }, height: '100%' }}>
            <CardContent>
              <Typography variant="subtitle1" gutterBottom>
                Preview panel
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Select a file to view a live preview. Supported formats include PDF, image, and Excel exports.
              </Typography>
              <Box
                sx={{
                  mt: 3,
                  minHeight: 220,
                  borderRadius: 2,
                  border: '1px dashed',
                  borderColor: 'grey.300',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  bgcolor: 'grey.50',
                }}
              >
                <Stack spacing={1} alignItems="center">
                  <InsertDriveFileIcon color="disabled" />
                  <Typography variant="body2" color="text.secondary">
                    Select a file to preview
                  </Typography>
                </Stack>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
