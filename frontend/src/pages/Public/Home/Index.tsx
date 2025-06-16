import LayoutDefault from '@/layouts/LayoutDefault';
import { HomePageProps } from './HomePageProps';
import { InternalLink } from '@/components/InternalLink';


export default function Index() {
  return (
    <>
      <div className='flex flex-col gap-y-24 max-w-7xl mx-auto pt-12 lg:pt-32 px-4'>
        <h1 className='font-bold text-4xl text-black mb-6'>
          PAUL
        </h1>
        <InternalLink name='Log in' to='/app/user/login/' />.
      </div>
    </>
  );
}

Index.layout = LayoutDefault;
