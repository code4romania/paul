import { Page } from '@inertiajs/core';
import classNames from 'classnames';
import { ReactNode } from 'react';
import { DashboardNavBars } from '@/components/DashboardNavBars';
import { Notification } from '@/components/Notification';
import { CommonProps } from '@/types/CommonProps';

export default function LayoutBackOffice(page: Page<CommonProps>) {
  const {
    props: { is_authenticated = false },
  } = page;

  return (
    <div className='flex flex-col h-full'>
      <DashboardNavBars />
      <main
        className={classNames(
          'grow mt-16 relative',
          is_authenticated && 'xl:pl-72 py-10',
        )}
      >
        {page as unknown as ReactNode}
        <Notification />
      </main>
    </div>
  );
}
