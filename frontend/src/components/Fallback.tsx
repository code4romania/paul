import { StructError } from 'superstruct';
import { Dialog } from './Dialog';
import { DialogContent } from './DialogContent';
import { DialogTitle } from './DialogTitle';
import { useState } from 'react';
import { useErrorBoundary } from 'react-error-boundary';
import { DialogFooter } from './DialogFooter';

export function Fallback({ error }: { error: Error }) {
  const [open, setOpen] = useState(true);
  const { resetBoundary } = useErrorBoundary();

  return (
    <div role='alert' className='flex flex-col mt-10 px-10'>
      <Dialog open={open}>
        <DialogTitle
          title={
            error instanceof StructError
              ? ' Validation of returned data has failed'
              : 'Something went wrong'
          }
          onClose={() => setOpen(false)}
        />
        <DialogContent>
          {error instanceof StructError ? (
            <>
              <div className='flex flex-col gap-4'>
                {error.failures().map((e) => (
                  <div
                    key={e.key}
                    className='border-l-4 border-l-error px-4 py-2 rounded-md shadow-md flex flex-col gap-1'
                  >
                    <div className='flex gap-2'>
                      <div className='font-amalia-medium'>Message:</div>
                      <pre className='text-error'>{e.message}</pre>
                    </div>
                    <div className='flex gap-2'>
                      <div className='font-amalia-medium'>Property:</div>
                      <pre className='bg-slate-100 rounded'>{e.key}</pre>
                    </div>
                    <div className='flex gap-2'>
                      <div className='font-amalia-medium'>Type:</div>
                      <pre className='bg-slate-100 rounded'>{e.type}</pre>
                    </div>
                    <div className='flex gap-2'>
                      <div className='font-amalia-medium'>Received value:</div>
                      <pre className='bg-slate-100 rounded break-all whitespace-normal'>
                        {e.value
                          ? JSON.stringify(e.value)
                          : 'undefined or null'}
                      </pre>
                    </div>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <>
              <p>Something went wrong when rendering the page</p>
              <pre style={{ color: 'red' }}>{error.message}</pre>
            </>
          )}
        </DialogContent>
        <DialogFooter
          mainButton={{ label: 'Refresh', onClick: resetBoundary }}
        />
      </Dialog>
    </div>
  );
}
