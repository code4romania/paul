import { ReactNode } from 'react';

type DialogContentProps = {
  children: ReactNode;
};

export function DialogContent({ children }: DialogContentProps) {
  return <div className='p-6 overflow-y-auto text-black'>{children}</div>;
}
