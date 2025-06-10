import LayoutDefault from '@/layouts/LayoutDefault';
import { HomePageProps } from './HomePageProps';


export default function Index({ cms }: HomePageProps) {
  return (
    <>
      <div className='flex flex-col gap-y-24 max-w-7xl mx-auto pt-12 lg:pt-32 px-4'>
      </div>
    </>
  );
}

Index.layout = LayoutDefault;
