import { useState } from 'react';
import { CommonProps } from '@/types/CommonProps';
import { DashboardSidebar } from './DashboardSidebar';
import { DashboardTopBar } from './DashboardTopBar';
import { usePage } from '@inertiajs/react';

export function DashboardNavBars() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const {
    props: { is_authenticated },
  } = usePage<CommonProps>();

  return (
    <>
      <DashboardTopBar handleOpenSidebar={() => setSidebarOpen(true)} />
      {is_authenticated && (
        <DashboardSidebar
          handleClose={() => setSidebarOpen(false)}
          open={sidebarOpen}
        />
      )}
    </>
  );
}
