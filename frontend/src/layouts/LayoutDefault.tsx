import { Page } from '@inertiajs/core';
import { ReactNode, useState } from 'react';
import { Button } from '@/components/Button';
import { Notification } from '@/components/Notification';
import { CommonProps } from '@/types/CommonProps';


export default function LayoutDefault(page: Page<CommonProps>) {
  return (
    <div className='flex flex-col h-full'>
      <main className='grow text-black'>
        {page as unknown as ReactNode}
        <Notification />
      </main>
    </div>
  );
}
