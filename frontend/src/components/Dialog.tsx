import { ReactNode } from 'react';

type DialogProps = {
  children: ReactNode;
  open: boolean;
};

export function Dialog({ children, open }: DialogProps) {
  if (!open) {
    return null;
  }

  return (
    <>
      <div className='w-full h-[100vh] fixed top-0 left-0 z-[70] overflow-x-hidden overflow-y-auto flex items-center'>
        <div className='md:max-w-3xl w-full m-3 md:mx-auto'>
          <div className='flex flex-col bg-white shadow-sm rounded-xl max-h-screen'>
            {children}
          </div>
        </div>
      </div>
      <div className='fixed inset-0 z-[60] bg-gray-800 bg-opacity-30' />
    </>
  );
}
